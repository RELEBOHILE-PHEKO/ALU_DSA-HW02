const fs = require('fs'); // Import the 'fs' module for reading from and writing to files

// SparseMatrix class definition
class SparseMatrix {
  // Constructor accepts either a file path (to load a matrix) or row and column numbers for manual creation
  constructor(rowsOrFilePath, cols = null) {
    this.rows = 0;
    this.cols = 0;
    this.matrix = {}; // Object to store the sparse matrix elements

    // Check if the argument is a string (file path); if so, load the matrix from the file
    if (typeof rowsOrFilePath === 'string') {
      this.loadMatrixFromFile(rowsOrFilePath);
    } else {
      // Otherwise, use the provided rows and columns to initialize an empty matrix
      this.rows = rowsOrFilePath;
      this.cols = cols;
    }
  }

  // Method to load a matrix from a file
  loadMatrixFromFile(matrixFilePath) {
    try {
      const fileContent = fs.readFileSync(matrixFilePath, 'utf8'); // Read the file content as a string
      const lines = fileContent.split('\n'); // Split file content by lines

      // Extract the number of rows from the first line of the file
      const rowMatch = lines[0].match(/rows=(\d+)/);
      // Extract the number of columns from the second line of the file
      const colMatch = lines[1].match(/cols=(\d+)/);

      // Throw an error if rows or columns information is missing
      if (!rowMatch || !colMatch) {
        throw new Error('Invalid file format: rows or cols not found');
      }

      this.rows = parseInt(rowMatch[1]); // Store the number of rows
      this.cols = parseInt(colMatch[1]); // Store the number of columns

      // Loop through the remaining lines (matrix elements)
      for (let i = 2; i < lines.length; i++) {
        const element = lines[i].trim(); // Remove any extra whitespace
        if (element.length > 0) {
          // Match the line format (row, col, value) using regex
          const match = element.match(/\((\d+),\s*(\d+),\s*(-?\d+)\)/);
          if (!match) {
            throw new Error('Input file has wrong format');
          }
          const [, row, col, value] = match.map(Number); // Extract row, col, value as numbers
          this.setElement(row, col, value); // Set the matrix element in the sparse matrix
        }
      }
    } catch (error) {
      throw new Error(`Error loading matrix from file: ${error.message}`); // Catch and throw file-related errors
    }
  }

  // Get the value of the matrix at a specific position (returns 0 if not set)
  getElement(row, col) {
    return this.matrix[`${row},${col}`] || 0;
  }

  // Set a value at a specific position in the matrix (remove if value is 0)
  setElement(row, col, value) {
    if (value !== 0) {
      this.matrix[`${row},${col}`] = value; // Store non-zero values
    } else {
      delete this.matrix[`${row},${col}`]; // Delete the entry if value is 0
    }
  }

  // Add two sparse matrices
  add(matrix) {
    // Check if the dimensions match
    if (this.rows !== matrix.rows || this.cols !== matrix.cols) {
      throw new Error('Matrices must have the same dimensions for addition');
    }
    const result = new SparseMatrix(this.rows, this.cols); // Create a new result matrix
    // Add elements from the first matrix
    for (const key in this.matrix) {
      const [row, col] = key.split(',').map(Number);
      result.setElement(row, col, this.getElement(row, col) + matrix.getElement(row, col));
    }
    // Add elements from the second matrix that are not in the first
    for (const key in matrix.matrix) {
      const [row, col] = key.split(',').map(Number);
      if (!(key in this.matrix)) {
        result.setElement(row, col, matrix.getElement(row, col));
      }
    }
    return result;
  }

  // Subtract two sparse matrices
  subtract(matrix) {
    // Check if the dimensions match
    if (this.rows !== matrix.rows || this.cols !== matrix.cols) {
      throw new Error('Matrices must have the same dimensions for subtraction');
    }
    const result = new SparseMatrix(this.rows, this.cols); // Create a new result matrix
    // Subtract elements of the second matrix from the first
    for (const key in this.matrix) {
      const [row, col] = key.split(',').map(Number);
      result.setElement(row, col, this.getElement(row, col) - matrix.getElement(row, col));
    }
    // Handle elements in the second matrix that are not in the first
    for (const key in matrix.matrix) {
      const [row, col] = key.split(',').map(Number);
      if (!(key in this.matrix)) {
        result.setElement(row, col, -matrix.getElement(row, col));
      }
    }
    return result;
  }

  // Multiply two sparse matrices
  multiply(matrix) {
    // Check if the number of columns in the first matrix matches the number of rows in the second
    if (this.cols !== matrix.rows) {
      throw new Error('Number of columns in the first matrix must be equal to the number of rows in the second matrix');
    }
    const result = new SparseMatrix(this.rows, matrix.cols); // Create a result matrix
    // Multiply elements based on matrix multiplication rules
    for (const key1 in this.matrix) {
      const [row1, col1] = key1.split(',').map(Number);
      for (const key2 in matrix.matrix) {
        const [row2, col2] = key2.split(',').map(Number);
        if (col1 === row2) { // Column of first matrix must match row of second matrix
          const product = this.matrix[key1] * matrix.matrix[key2];
          const currentValue = result.getElement(row1, col2);
          result.setElement(row1, col2, currentValue + product); // Accumulate the sum of products
        }
      }
    }
    return result;
  }

  // Print the matrix in a readable format
  print() {
    console.log(`Matrix (${this.rows}x${this.cols}):`);
    for (let i = 0; i < this.rows; i++) {
      let row = '';
      for (let j = 0; j < this.cols; j++) {
        row += (this.getElement(i, j) + ' ').padStart(8); // Format the row for readability
      }
      console.log(row); // Print each row
    }
  }
}

// Main function to run the program
function main() {
  try {
    console.log("Loading matrices...");
    const matrix1 = new SparseMatrix('sample_inputs/matrixfile1.txt'); // Load matrix 1 from a file
    const matrix3 = new SparseMatrix('sample_inputs/matrixfile3.txt'); // Load matrix 3 from a file

    console.log("\nMatrix 1 (from matrixfile1.txt):");
    matrix1.print(); // Print matrix 1

    console.log("\nMatrix 3 (from matrixfile3.txt):");
    matrix3.print(); // Print matrix 3

    console.log("\nPerforming matrix operations...");

    // Perform addition
    console.log("\nAddition Result (Matrix 1 + Matrix 3):");
    try {
      const addResult = matrix1.add(matrix3); // Add matrices
      addResult.print(); // Print the addition result
    } catch (error) {
      console.error("Addition Error:", error.message); // Handle any addition errors
    }

    // Perform subtraction
    console.log("\nSubtraction Result (Matrix 1 - Matrix 3):");
    try {
      const subResult = matrix1.subtract(matrix3); // Subtract matrices
      subResult.print(); // Print the subtraction result
    } catch (error) {
      console.error("Subtraction Error:", error.message); // Handle any subtraction errors
    }

    // Perform multiplication
    console.log("\nMultiplication Result (Matrix 1 * Matrix 3):");
    try {
      const mulResult = matrix1.multiply(matrix3); // Multiply matrices
      mulResult.print(); // Print the multiplication result
    } catch (error) {
      console.error("Multiplication Error:", error.message); // Handle any multiplication errors
    }

  } catch (error) {
    console.error("Error:", error.message); // Handle any errors during file loading or matrix operations
  }
}

// Run the main function
main();
