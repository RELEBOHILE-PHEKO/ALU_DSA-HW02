# Sparse Matrix

## Overview

The Sparse Matrix project implements a data structure and operations for managing large sparse matrices in JavaScript. Sparse matrices are matrices in which most of the elements are zero. This implementation focuses on optimizing memory usage and performance when storing and manipulating such matrices.

## Features

- **Matrix Representation**: Uses a `Map` to store non-zero elements, reducing memory consumption significantly compared to traditional 2D array representations.
- **Matrix Operations**:
  - **Addition**: Adds two sparse matrices of the same dimensions.
  - **Subtraction**: Subtracts one sparse matrix from another of the same dimensions.
  - **Multiplication**: Multiplies two matrices, adhering to the matrix multiplication rules.
- **File Input**: Loads sparse matrices from a well-defined input file format.
- **Error Handling**: Custom error handling for:
  - Incorrect matrix dimensions during operations.
  - Invalid file formats.

## File Format

The input file for the sparse matrices must follow this specific format:


### Example Input File

```plaintext
rows=8433
cols=3180
(0, 381, -694)
(0, 128, -838)
(0, 639, 857)
(0, 165, -933)
(0, 1350, -89)

First Line: Indicates the total number of rows in the matrix.
Second Line: Indicates the total number of columns in the matrix.
Subsequent Lines: Each line specifies a non-zero element in the matrix in the format (row, column, value).
