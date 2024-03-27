import { spawn, exec } from 'child_process';

export const spawnPython = (filePath: string, script: string) => {
    return new Promise((resolve, reject) => {
        const python = spawn('python', [filePath, script]);
        var result = '';
        python.stdout.on('data', (data: any) => {
            result += data.toString();
        });

        python.on('close', () => {
            console.log(result);
            resolve(result);
        });
        python.on('error', (err: any) => {
            reject(err);
        });
    })
};

export const execPython = (filePath: string, inputPath: string, outputPath: string) => {
    return new Promise((resolve, reject) => {
        exec(`python ${filePath} ${inputPath} ${outputPath}`, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error: ${error.message}`);
                reject(error);
            }
            resolve(stdout || null);
        });
    })
}