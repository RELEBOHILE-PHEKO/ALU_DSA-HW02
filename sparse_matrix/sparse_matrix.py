// ... (previous SparseMatrix class code remains the same)

// Example usage
function main() {
    try {
        // Load matrices from files
        const matrix1 = new SparseMatrix('sample_inputs/matrixfile1.txt');
        const matrix3 = new SparseMatrix('sample_inputs/matrixfile3.txt');

        // Perform operations
        const addResult = matrix1.add(matrix3);
        const subtractResult = matrix1.subtract(matrix3);
        const multiplyResult = matrix1.multiply(matrix3);

        // Output results
        console.log('Addition Result:\n' + addResult.toString());
        console.log('Subtraction Result:\n' + subtractResult.toString());
        console.log('Multiplication Result:\n' + multiplyResult.toString());
    } catch (error) {
        console.error('Error:', error.message);
        // Add more detailed error logging
        console.error('Stack trace:', error.stack);
    }
}

main();
