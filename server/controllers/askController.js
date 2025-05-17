// import { PythonShell } from 'python-shell';
// import { fileURLToPath } from 'url';
// import { dirname, join } from 'path';
// import fs from 'fs/promises';

// const __filename = fileURLToPath(import.meta.url);
// const __dirname = dirname(__filename);

// export async function handleQuestion(message) {
//   try {
//     const scriptPath = join(__dirname, '..', 'scripts', 'main.py');
//     const modelPath = join(__dirname, '..', 'models');
//     const textPath = join(__dirname, '..', 'text_data');

//     // Check if required files exist
//     try {
//       await fs.access(scriptPath);
//       await fs.access(modelPath);
//       await fs.access(textPath);
//     } catch (error) {
//       return {
//         answer: "Required files are missing. Please ensure model files, text files, and Python script are properly uploaded."
//       };
//     }

//     const options = {
//       mode: 'text',
//       pythonPath: 'python3',
//       pythonOptions: ['-u'],
//       scriptPath: dirname(scriptPath),
//       args: [
//         message,
//         modelPath,
//         textPath
//       ]
//     };

//     const results = await PythonShell.run('main.py', options);
//     return { answer: results[0] };
//   } catch (error) {
//     console.error('Error processing question:', error);
//     throw new Error('Failed to process question: ' + error.message);
//   }
// }
import { PythonShell } from 'python-shell';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import fs from 'fs/promises';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export async function handleQuestion(message) {
  try {
    const scriptPath = "project3\project\server\scripts\main.py";
    const modelPath = "project3\project\server\models";
    const textPath = "project3\project\server\text_data";
  

    // Check if required files exist
    try {
      await fs.access(scriptPath);
      await fs.access(modelPath);
      await fs.access(textPath);
    } catch (error) {
      return {
        answer: "Required files are missing. Please ensure model files, text files, and Python script are properly uploaded."
      };
    }

    // Log paths for debugging
    console.log('Script Path:', scriptPath);
    console.log('Model Path:', modelPath);
    console.log('Text Path:', textPath);

    const options = {
      mode: 'text',
      pythonPath: 'python3', // or 'python3', based on your setup
      pythonOptions: ['-u'],
      scriptPath: dirname(scriptPath),
      args: [
        message,
        modelPath,
        textPath
      ]
    };

    // Run the Python script
    const results = await PythonShell.run('main.py', options);
    console.log('Python script result:', results); // Log result for debugging

    return { answer: results[0] };
  } catch (error) {
    console.error('Error processing question:', error);
    throw new Error('Failed to process question: ' + error.message);
  }
}
