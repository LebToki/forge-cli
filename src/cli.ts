#!/usr/bin/env node

import { Command } from 'commander';
import { showGlassBanner, glassSpinner, glassPanel } from './ui/glassmorphic.js';
import { DeepSeekClient } from './core/deepseek.js';
import dotenv from 'dotenv';
import chalk from 'chalk';
import fs from 'fs/promises';
import path from 'path';

dotenv.config();

const program = new Command();

program
  .name('forge')
  .description('🔥 FORGE - Glassmorphic AI Development Ecosystem')
  .version('0.1.0');

program
  .command('ask')
  .description('Ask DeepSeek anything')
  .argument('<prompt...>', 'Your question')
  .option('-f, --file <files...>', 'Include file context')
  .action(async (prompt: string[], options) => {
    const question = prompt.join(' ');
    const spinner = glassSpinner('🔮 FORGE is thinking...');
    spinner.start();
    
    try {
      const client = new DeepSeekClient();
      
      let files: string[] = [];
      if (options.file) {
        for (const file of options.file) {
          try {
            const content = await fs.readFile(file, 'utf-8');
            files.push(`File: ${file}\n\`\`\`\n${content}\n\`\`\``);
          } catch (e) {
            console.log(chalk.red(`Error reading file: ${file}`));
          }
        }
      }
      
      const response = await client.ask(question, files);
      spinner.succeed('✨ FORGE responds:');
      
      console.log(glassPanel(response, 'DeepSeek says'));
    } catch (error) {
      spinner.fail(`💥 Error: ${error}`);
    }
  });

program
  .command('chat')
  .description('Interactive chat with DeepSeek')
  .action(async () => {
    await showGlassBanner();
    console.log(glassPanel('Starting interactive session... Type "exit" to quit', '💬 Chat Mode'));
    
    const client = new DeepSeekClient();
    await client.interactiveChat();
  });

program
  .command('generate')
  .description('Generate code with AI')
  .argument('<description...>', 'What to generate')
  .option('-l, --language <lang>', 'Programming language', 'typescript')
  .action(async (description: string[], options) => {
    const prompt = description.join(' ');
    const spinner = glassSpinner('🔥 FORGE is generating code...');
    spinner.start();
    
    try {
      const client = new DeepSeekClient();
      const code = await client.generate(`Generate ${options.language} code for: ${prompt}`);
      spinner.succeed('✨ Code generated!');
      
      console.log(glassPanel(code, `${options.language} Code`));
    } catch (error) {
      spinner.fail(`💥 Error: ${error}`);
    }
  });

program
  .command('php')
  .description('PHP/WordPress commands')
  .argument('<action>', 'Action: plugin, theme, analyze')
  .argument('[args...]', 'Additional arguments')
  .action(async (action: string, args: string[]) => {
    const spinner = glassSpinner(`⚡ FORGE PHP: ${action}...`);
    spinner.start();
    
    try {
      const client = new DeepSeekClient();
      
      if (action === 'plugin') {
        const pluginName = args[0] || 'my-plugin';
        const description = args.slice(1).join(' ') || 'A custom WordPress plugin';
        
        const prompt = `Generate a complete WordPress plugin:
        Name: ${pluginName}
        Description: ${description}
        
        Include:
        - Plugin header with proper metadata
        - Admin menu setup
        - Shortcode implementation
        - Proper security (escaping, nonces)
        - Internationalization ready`;
        
        const code = await client.generate(prompt);
        spinner.succeed('✨ Plugin generated!');
        console.log(glassPanel(code, `WordPress Plugin: ${pluginName}`));
        
      } else if (action === 'theme') {
        const themeName = args[0] || 'my-theme';
        const prompt = `Generate a WordPress theme structure for: ${themeName}`;
        const code = await client.generate(prompt);
        spinner.succeed('✨ Theme generated!');
        console.log(glassPanel(code, `WordPress Theme: ${themeName}`));
        
      } else {
        spinner.fail('⚠️ Unknown action. Use: plugin, theme, or analyze');
      }
    } catch (error) {
      spinner.fail(`💥 Error: ${error}`);
    }
  });

program.parse(process.argv);
