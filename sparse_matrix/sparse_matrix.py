const fs = require('fs');

class SparseMatrix {
    constructor(rowsOrFilePath, cols = null) {
        // Store non-zero elements in a Map for efficient memory usage
        this.elements = new Map();
        
        if (typeof rowsOrFilePath === 'string') {
            // If a file path is provided, load the matrix from the file
            this.loadFromFile(rowsOrFilePath);
        } else {
            // Otherwise, create an empty matrix with given dimensions
            this.rows = rowsOrFilePath;
            this.cols = cols;
        }
    }

    loadFromFile(filePath) {
        // Read the file content
        const content = fs.readFileSync(filePath, 'utf8');
        const lines = content.split('\n').map(line => line.trim()).filter(line => line);

        // Parse rows and columns
        this.rows = parseInt(lines[0].split('=')[1]);
        this.cols = parseInt(lines[1].split('=')[1]);

        // Parse and store non-zero elements
        for (let i = 2; i < lines.length; i++) {
            const [row, col, value] = lines[i].slice(1, -1).split(',').map(Number);
            this.set(row, col, value);
        }
    }

    // Get the value at a specific position
    get(row, col) {
        return this.elements.get(`${row},${col}`) || 0;
    }

    // Set a value at a specific position
    set(row, col, value) {
        if (value !== 0) {
            this.elements.set(`${row},${col}`, value);
        } else {
            this.elements.delete(`${row},${col}`);
        }
    }

    // Add two matrices
    add(other) {
        if (this.rows !== other.rows || this.cols !== other.cols) {
            throw new Error('Matrix dimensions must match for addition');
        }

        const result = new SparseMatrix(this.rows, this.cols);

        // Add elements from both matrices
        for (let row = 0; row < this.rows; row++) {
            for (let col = 0; col < this.cols; col++) {
                const sum = this.get(row, col) + other.get(row, col);
                if (sum !== 0) {
                    result.set(row, col, sum);
                }
            }
        }

        return result;
    }

    // Subtract one matrix from another
    subtract(other) {
        if (this.rows !== other.rows || this.cols !== other.cols) {
            throw new Error('Matrix dimensions must match for subtraction');
        }

        const result = new SparseMatrix(this.rows, this.cols);

        // Subtract elements
        for (let row = 0; row < this.rows; row++) {
            for (let col = 0; col < this.cols; col++) {
                const diff = this.get(row, col) - other.get(row, col);
                if (diff !== 0) {
                    result.set(row, col, diff);
                }
            }
        }

        return result;
    }

    // Multiply two matrices
    multiply(other) {
        if (this.cols !== other.rows) {
            throw new Error('Number of columns in first matrix must equal number of rows in second matrix');
        }

        const result = new SparseMatrix(this.rows, other.cols);

        // Perform matrix multiplication
        for (let row = 0; row < this.rows; row++) {
            for (let col = 0; col < other.cols; col++) {
                let sum = 0;
                for (let k = 0; k < this.cols; k++) {
                    sum += this.get(row, k) * other.get(k, col);
                }
                if (sum !== 0) {
                    result.set(row, col, sum);
                }
            }
        }

        return result;
    }

    // Convert matrix to string representation
    toString() {
        let result = `rows=${this.rows}\ncols=${this.cols}\n`;
        for (const [key, value] of this.elements) {
            const [row, col] = key.split(',');
            result += `(${row}, ${col}, ${value})\n`;
        }
        return result;
    }
}

// Example usage
function main() {
    try {
        // Load matrices from files
        const matrix1 = new SparseMatrix('matrixfile1.txt');
        const matrix2 = new SparseMatrix('matrixfile3.txt');

        // Perform operations
        const addResult = matrix1.add(matrix3);
        const subtractResult = matrix1.subtract(matrix2);
        const multiplyResult = matrix1.multiply(matrix2);

        // Output results
        console.log('Addition Result:\n' + addResult.toString());
        console.log('Subtraction Result:\n' + subtractResult.toString());
        console.log('Multiplication Result:\n' + multiplyResult.toString());
    } catch (error) {
        console.error('Error:', error.message);
    }
}

main();
