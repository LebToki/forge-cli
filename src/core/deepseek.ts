import OpenAI from 'openai';

export class DeepSeekClient {
  private client: OpenAI;
  
  constructor(apiKey?: string) {
    this.client = new OpenAI({
      apiKey: apiKey || process.env.DEEPSEEK_API_KEY || '',
      baseURL: 'https://api.deepseek.com'
    });
  }
  
  async ask(question: string, files?: string[]): Promise<string> {
    const messages: OpenAI.Chat.ChatMessage[] = [
      {
        role: 'system',
        content: 'You are FORGE, an AI coding assistant. Help with code, answer questions, and provide expert guidance.'
      }
    ];
    
    if (files && files.length > 0) {
      let context = 'Here are the files I\'m working with:\n\n';
      for (const file of files) {
        context += `File: ${file}\n`;
      }
      context += `\nQuestion: ${question}`;
      messages.push({ role: 'user', content: context });
    } else {
      messages.push({ role: 'user', content: question });
    }
    
    const response = await this.client.chat.completions.create({
      model: 'deepseek-chat',
      messages,
      temperature: 0.7,
      max_tokens: 4096
    });
    
    return response.choices[0]?.message?.content || 'No response';
  }
  
  async *streamAsk(question: string, files?: string[]): AsyncGenerator<string> {
    const messages: OpenAI.Chat.ChatMessage[] = [
      {
        role: 'system',
        content: 'You are FORGE, an AI coding assistant. Help with code, answer questions, and provide expert guidance.'
      }
    ];
    
    if (files && files.length > 0) {
      let context = 'Here are the files I\'m working with:\n\n';
      for (const file of files) {
        context += `File: ${file}\n`;
      }
      context += `\nQuestion: ${question}`;
      messages.push({ role: 'user', content: context });
    } else {
      messages.push({ role: 'user', content: question });
    }
    
    const stream = await this.client.chat.completions.create({
      model: 'deepseek-chat',
      messages,
      temperature: 0.7,
      max_tokens: 4096,
      stream: true
    });
    
    for await (const chunk of stream) {
      const content = chunk.choices[0]?.delta?.content;
      if (content) {
        yield content;
      }
    }
  }
  
  async generate(prompt: string): Promise<string> {
    const messages: OpenAI.Chat.ChatMessage[] = [
      {
        role: 'system',
        content: 'You are FORGE, an expert code generator. Generate clean, well-documented code based on the request.'
      },
      {
        role: 'user',
        content: prompt
      }
    ];
    
    const response = await this.client.chat.completions.create({
      model: 'deepseek-chat',
      messages,
      temperature: 0.5,
      max_tokens: 8192
    });
    
    return response.choices[0]?.message?.content || '';
  }
  
  async interactiveChat(): Promise<void> {
    const readline = await import('readline');
    
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });
    
    const history: OpenAI.Chat.ChatMessage[] = [
      {
        role: 'system',
        content: 'You are FORGE, an AI coding assistant. Help with code, answer questions, and provide expert guidance.'
      }
    ];
    
    const askQuestion = (): void => {
      rl.question('\n🔮 You: ', async (input) => {
        if (input.toLowerCase() === 'exit') {
          console.log('\n👋 Goodbye!');
          rl.close();
          return;
        }
        
        history.push({ role: 'user', content: input });
        
        try {
          const stream = await this.client.chat.completions.create({
            model: 'deepseek-chat',
            messages: history,
            temperature: 0.7,
            max_tokens: 4096,
            stream: true
          });
          
          process.stdout.write('\n🔥 FORGE: ');
          for await (const chunk of stream) {
            const content = chunk.choices[0]?.delta?.content;
            if (content) {
              process.stdout.write(content);
            }
          }
          console.log('\n');
        } catch (error) {
          console.error('\n❌ Error:', error);
        }
        
        askQuestion();
      });
    };
    
    askQuestion();
  }
}
