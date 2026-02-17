// @ts-ignore - chalk-animation has no types
import chalkAnimation from 'chalk-animation';
// @ts-ignore - gradient-string has no types
import gradient from 'gradient-string';
import chalk from 'chalk';
import figlet from 'figlet';
import boxen from 'boxen';
import ora from 'ora';

// Glassmorphic color schemes
export const glassTheme = {
  primary: gradient(['#8ec5fc', '#e0c3fc']),
  secondary: gradient(['#fbc2eb', '#a6c1ee']),
  success: gradient(['#84fab0', '#8fd3f4']),
  warning: gradient(['#fad0c4', '#ffd1ff']),
  error: gradient(['#ff9a9e', '#fecfef']),
  glass: 'rgba(255, 255, 255, 0.25)',
  glassBorder: 'rgba(255, 255, 255, 0.4)',
};

// Sexy glassmorphic banner
export async function showGlassBanner(): Promise<void> {
  console.clear();
  
  const bannerText = figlet.textSync('FORGE', {
    font: 'ANSI Shadow',
    horizontalLayout: 'full'
  });
  
  const gradientBanner = gradient(['#8ec5fc', '#e0c3fc', '#fbc2eb'])(bannerText);
  
  const banner = boxen(gradientBanner, {
    padding: 1,
    margin: 1,
    borderStyle: 'round',
    borderColor: 'cyan',
    backgroundColor: 'rgba(255,255,255,0.1)',
    title: '🔥 GLASS FORGE',
    titleAlignment: 'center'
  });
  
  console.log(banner);
  
  const subtitle = chalkAnimation.rainbow('\n⚡ Shape Code • Ship Faster • Look Sexy ⚡\n');
  await new Promise(resolve => setTimeout(resolve, 2000));
  subtitle.stop();
}

// Glassmorphic spinner
export function glassSpinner(text: string) {
  return ora({
    text: gradient(['#8ec5fc', '#e0c3fc'])(text),
    color: 'cyan',
    spinner: 'dots'
  });
}

// Glassmorphic panel
export function glassPanel(content: string, title?: string): string {
  return boxen(content, {
    padding: 1,
    margin: 1,
    borderStyle: 'round',
    borderColor: 'cyan',
    backgroundColor: '#1a1a2e',
    title: title ? gradient(['#8ec5fc', '#e0c3fc'])(title) : undefined,
    titleAlignment: 'center'
  });
}

// Glassmorphic progress bar
export function glassProgress(current: number, total: number, width: number = 40): string {
  const percent = current / total;
  const filled = Math.round(width * percent);
  const empty = width - filled;
  
  const filledBar = '█'.repeat(filled).split('').map(c => 
    gradient(['#8ec5fc', '#e0c3fc'])(c)
  ).join('');
  
  const emptyBar = '░'.repeat(empty);
  
  return `[${filledBar}${emptyBar}] ${Math.round(percent * 100)}%`;
}
