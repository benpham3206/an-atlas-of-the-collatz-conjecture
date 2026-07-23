/* Transport kernel for the plateau-drift-test packet.
 *
 * Computes the Syracuse-character recursion on half-unit-indexed complex128
 * state (provenance: the recursion identity of the syracuse-fourier /
 * scalar-phase packets, c_n(xi) = norm * sum_a 2^-a e(-xi u_a / 3^n)
 * c_{n-1}(xi u_a mod 3^(n-1)), re-derived and validated against dense FFT
 * in verify_plateau_drift_test.py):
 *
 *   Cnew[j] = norm * sum_{a=1..taps} w_a * phase_a(xi_j) * C_old(xi_j u_a mod 3^(n-1))
 *
 * where j <-> xi_j = 3*(j/2)+1+(j%2) enumerates units 0 < xi < 3^n/2,
 * C_old lookups use the conjugate symmetry c(-xi) = conj(c(xi)), and the
 * phase e^{-2 pi i nu / 3^n} is evaluated as Thi[nu / lo] * Tlo[nu % lo]
 * (two exact-root tables, float64, no fast-math).
 *
 * nu_a(xi) is carried INCREMENTALLY across consecutive j (xi increases by 1
 * or 2), so the inner loop has no 64-bit division: one add + conditional
 * subtract per tap. Deterministic: output element j depends only on j.
 *
 * Compiled by verify_plateau_drift_test.py with clang -O3 (IEEE semantics;
 * no -ffast-math). complex128 is passed as interleaved double pairs.
 */

#include <stdint.h>
#include <pthread.h>

typedef struct {
    const double *Cold;   /* 2 * h_old interleaved re,im */
    double *Cnew;         /* 2 * h_new */
    uint64_t mod_old;     /* 3^(n-1) */
    uint64_t mod_new;     /* 3^n */
    const uint64_t *u;    /* u[a] = 2^-a mod mod_new, a = 1..taps */
    const double *w;      /* w[a] = 2^-a */
    int taps;
    const double *Thi;    /* 2 * hi_size, Thi[q] = e^{-2 pi i q / hi_size} */
    const double *Tlo;    /* 2 * lo_size, Tlo[r] = e^{-2 pi i r / mod_new} */
    uint64_t lo_size;
    double norm;
    uint64_t j0, j1;      /* output index range for this thread */
} job_t;

static void run_range(job_t *J)
{
    const uint64_t mod_new = J->mod_new;
    const uint64_t mod_old = J->mod_old;
    const uint64_t two_mod_old = 2 * mod_old;
    const int taps = J->taps;
    const uint64_t lo = J->lo_size;
    uint64_t nuv[64];     /* carried nu_a = xi * u_a mod mod_new */
    double accr = 0.0, acci = 0.0;

    uint64_t j = J->j0;
    uint64_t xi = 3 * (j / 2) + 1 + (j % 2);
    for (int a = 1; a <= taps; a++)
        nuv[a] = (xi * J->u[a]) % mod_new;

    for (; j < J->j1; j++) {
        accr = 0.0;
        acci = 0.0;
        for (int a = 1; a <= taps; a++) {
            uint64_t nu = nuv[a];
            /* mu = nu mod mod_old, with mod_new = 3 * mod_old */
            uint64_t mu = nu;
            if (mu >= mod_old) mu -= mod_old;
            if (mu >= mod_old) mu -= mod_old;
            /* conjugate-symmetry fold into the stored half */
            int flip = 2 * mu > mod_old;
            uint64_t m2 = flip ? mod_old - mu : mu;
            uint64_t jj = 2 * (m2 / 3) + (m2 % 3 == 2);
            double vr = J->Cold[2 * jj];
            double vi = J->Cold[2 * jj + 1];
            if (flip) vi = -vi;
            /* phase = Thi[nu / lo] * Tlo[nu % lo] */
            uint64_t q = nu / lo;
            uint64_t r = nu - q * lo;
            double hr = J->Thi[2 * q], hi = J->Thi[2 * q + 1];
            double lr = J->Tlo[2 * r], li = J->Tlo[2 * r + 1];
            double pr = hr * lr - hi * li;
            double pi = hr * li + hi * lr;
            double wa = J->w[a];
            accr += wa * (pr * vr - pi * vi);
            acci += wa * (pr * vi + pi * vr);
            /* carry nu_a to the next j: xi increases by 1 (j even) or 2 */
            nu += J->u[a];
            if (nu >= mod_new) nu -= mod_new;
            if (j & 1) {
                nu += J->u[a];
                if (nu >= mod_new) nu -= mod_new;
            }
            nuv[a] = nu;
        }
        J->Cnew[2 * j] = J->norm * accr;
        J->Cnew[2 * j + 1] = J->norm * acci;
    }
    (void)two_mod_old;
}

void transport(const double *Cold, double *Cnew,
               uint64_t mod_old, uint64_t mod_new, uint64_t h_new,
               const uint64_t *u, const double *w, int taps,
               const double *Thi, const double *Tlo, uint64_t lo_size,
               double norm, int nthreads)
{
    pthread_t tid[32];
    job_t jobs[32];
    if (nthreads < 1) nthreads = 1;
    if (nthreads > 32) nthreads = 32;
    uint64_t chunk = (h_new + (uint64_t)nthreads - 1) / (uint64_t)nthreads;
    int n = 0;
    for (int t = 0; t < nthreads; t++) {
        uint64_t j0 = (uint64_t)t * chunk;
        uint64_t j1 = j0 + chunk;
        if (j0 >= h_new) break;
        if (j1 > h_new) j1 = h_new;
        jobs[n] = (job_t){Cold, Cnew, mod_old, mod_new, u, w, taps,
                          Thi, Tlo, lo_size, norm, j0, j1};
        pthread_create(&tid[n], NULL, (void *(*)(void *))run_range, &jobs[n]);
        n++;
    }
    for (int t = 0; t < n; t++)
        pthread_join(tid[t], NULL);
}
