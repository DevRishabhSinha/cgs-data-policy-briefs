const fs = require('fs').promises;

class Queue {
    constructor() {
        this.items = [];
        this.processing = false;
    }

    async enqueue(task) {
        this.items.push(task);
        if (!this.processing) {
            await this.process();
        }
    }

    async process() {
        if (this.processing) return;
        this.processing = true;
        
        while (this.items.length > 0) {
            const task = this.items.shift();
            try {
                const currentData = await fs.readFile(task.filePath, 'utf8')
                    .then(data => JSON.parse(data))
                    .catch(() => ({}));
                
                Object.assign(currentData, task.data);
                
                await fs.writeFile(
                    task.filePath,
                    JSON.stringify(currentData, null, 2),
                    'utf8'
                );
            } catch (error) {
                console.error('Error processing file write task:', error);
            }
        }
        
        this.processing = false;
    }
}

module.exports = { Queue };