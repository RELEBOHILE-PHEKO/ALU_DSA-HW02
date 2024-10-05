const fs = require('fs');

class SparseMatrix {
  constructor(rowsOrFilePath, cols = null) {
    this.rows = 0;
    this.cols = 0;
    this.matrix = {};
    
    if (typeof rowsOrFilePath === 'string') {
      this.loadMatrixFromFile(rowsOrFilePath);
    } else {
      this.rows = rowsOrFilePath;
      this.cols = cols;
    }
  }

  loadMatrixFromFile(matrixFilePath) {
    try {
      const fileContent = fs.readFileSync(matrixFilePath, 'utf8');
      const lines = fileContent.split('\n');

      const rowMatch = lines[0].match(/rows=(\d+)/);
      const colMatch = lines[1].match(/cols=(\d+)/);
      
      if (!rowMatch || !colMatch) {
        throw new Error('Invalid file format: rows or cols not found');
      }

      this.rows = parseInt(rowMatch[1]);
      this.cols = parseInt(colMatch[1]);

      for (let i = 2; i < lines.length; i++) {
        const element = lines[i].trim();
        if (element.length > 0) {
          const match = element.match(/\((\d+),\s*(\d+),\s*(-?\d+)\)/);
          if (!match) {
            throw new Error('Input file has wrong format');
          }
          const [, row, col, value] = match.map(Number);
          this.setElement(row, col, value);
        }
      }
    } catch (error) {
      throw new Error(`Error loading matrix from file: ${error.message}`);
    }
  }

  getElement(row, col) {
    return this.matrix[`${row},${col}`] || 0;
  }

  setElement(row, col, value) {
    if (value !== 0) {
      this.matrix[`${row},${col}`] = value;
    } else {
      delete this.matrix[`${row},${col}`];
    }
  }

  add(matrix) {
    if (this.rows !== matrix.rows || this.cols !== matrix.cols) {
      throw new Error('Matrices must have the same dimensions for addition');
    }
    const result = new SparseMatrix(this.rows, this.cols);
    for (const key in this.matrix) {
      const [row, col] = key.split(',').map(Number);
      result.setElement(row, col, this.getElement(row, col) + matrix.getElement(row, col));
    }
    for (const key in matrix.matrix) {
      const [row, col] = key.split(',').map(Number);
      if (!(key in this.matrix)) {
        result.setElement(row, col, matrix.getElement(row, col));
      }
    }
    return result;
  }

  subtract(matrix) {
    if (this.rows !== matrix.rows || this.cols !== matrix.cols) {
      throw new Error('Matrices must have the same dimensions for subtraction');
    }
    const result = new SparseMatrix(this.rows, this.cols);
    for (const key in this.matrix) {
      const [row, col] = key.split(',').map(Number);
      result.setElement(row, col, this.getElement(row, col) - matrix.getElement(row, col));
    }
    for (const key in matrix.matrix) {
      const [row, col] = key.split(',').map(Number);
      if (!(key in this.matrix)) {
        result.setElement(row, col, -matrix.getElement(row, col));
      }
    }
    return result;
  }

  multiply(matrix) {
    if (this.cols !== matrix.rows) {
      throw new Error('Number of columns in the first matrix must be equal to the number of rows in the second matrix');
    }
    const result = new SparseMatrix(this.rows, matrix.cols);
    for (const key1 in this.matrix) {
      const [row1, col1] = key1.split(',').map(Number);
      for (const key2 in matrix.matrix) {
        const [row2, col2] = key2.split(',').map(Number);
        if (col1 === row2) {
          const product = this.matrix[key1] * matrix.matrix[key2];
          const currentValue = result.getElement(row1, col2);
          result.setElement(row1, col2, currentValue + product);
        }
      }
    }
    return result;
  }

  print() {
    console.log(`Matrix (${this.rows}x${this.cols}):`);
    for (let i = 0; i < this.rows; i++) {
      let row = '';
      for (let j = 0; j < this.cols; j++) {
        row += (this.getElement(i, j) + ' ').padStart(8);
      }
      console.log(row);
    }
  }
}

function main() {
  try {
    console.log("Loading matrices...");
    const matrix1 = new SparseMatrix('sample_inputs/matrixfile1.txt');
    const matrix3 = new SparseMatrix('sample_inputs/matrixfile3.txt');

    console.log("\nMatrix 1 (from matrixfile1.txt):");
    matrix1.print();

    console.log("\nMatrix 3 (from matrixfile3.txt):");
    matrix3.print();

    console.log("\nPerforming matrix operations...");

    console.log("\nAddition Result (Matrix 1 + Matrix 3):");
    try {
      const addResult = matrix1.add(matrix3);
      addResult.print();
    } catch (error) {
      console.error("Addition Error:", error.message);
    }

    console.log("\nSubtraction Result (Matrix 1 - Matrix 3):");
    try {
      const subResult = matrix1.subtract(matrix3);
      subResult.print();
    } catch (error) {
      console.error("Subtraction Error:", error.message);
    }

    console.log("\nMultiplication Result (Matrix 1 * Matrix 3):");
    try {
      const mulResult = matrix1.multiply(matrix3);
      mulResult.print();
    } catch (error) {
      console.error("Multiplication Error:", error.message);
    }

  } catch (error) {
    console.error("Error:", error.message);
  }
}

// Run the main function
main();
