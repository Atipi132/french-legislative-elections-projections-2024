const { spawn } = require('child_process');

function runPythonScript() {
    return new Promise((resolve, reject) => {
        // Spawn a child process to run the Python script
        const pythonProcess = spawn('python', ['main.py']);

        // Handle stdout data (optional)
        pythonProcess.stdout.on('data', (data) => {
            console.log(`stdout: ${data}`);
        });

        // Handle stderr data (optional)
        pythonProcess.stderr.on('data', (data) => {
            console.error(`stderr: ${data}`);
        });

        // Handle the close event to know when the script has finished
        pythonProcess.on('close', (code) => {
            if (code === 0) {
                resolve(`Python script finished with code ${code}`);
            } else {
                reject(`Python script finished with error code ${code}`);
            }
        });

        // Handle error event
        pythonProcess.on('error', (err) => {
            reject(`Failed to start Python script: ${err}`);
        });
    });
}

// Call the function and wait for it to complete
runPythonScript()
    .then((message) => {
        console.log(message);
    })
    .catch((error) => {
        console.error(error);
    });
