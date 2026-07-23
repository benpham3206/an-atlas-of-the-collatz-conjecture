# Motivation

This document states why this work exists. It uses controlled technical
language: short sentences, plain terms, one statement at a time.

## 1. Purpose

This repository is a test case. The goal is a repeatable method to attack
hard problems. The Collatz conjecture is the first problem under test. The
method is the product. Collatz is the sandbox.

## 2. Why Collatz

The Collatz rule is simple. A check of one example is simple. A general proof
is hard. This gap is the reason to use Collatz.

- A simple rule keeps the setup clear.
- A hard proof exposes the true cost of proof search.

A problem with this gap shows what real proof work requires. It does not hide
that cost behind a complex definition.

## 3. Origin

The problem first appeared on a whiteboard. The place was a multivariable
calculus workshop. The contrast between the simple rule and the hard proof
started this work.

## 4. Method principle

Treat a proof as a constraint system. Every definition, lemma, and result
must agree with every other one. One mismatch breaks the whole structure.

The following rules follow from this principle:

- Each result uses exact integer or rational arithmetic.
- Each result carries an independent check.
- Each result records its provenance.
- A measurement is labelled as a measurement, not as a theorem.

## 5. Working rule

Progress is the target. A single breakthrough is not the target.

- Add small results. Each result must be rigorous and verifiable.
- Enough verified progress raises the chance of a breakthrough.
- In some cases, enough verified progress forces a breakthrough.

## 6. Scope beyond Collatz

The method matters more than the single problem. The same method applies to
other hard problems. Examples:

- P versus NP.
- Proof search.
- Counterexample classification.
- A record of the reasoning process.

Collatz is the current test. The method is the transferable result.
