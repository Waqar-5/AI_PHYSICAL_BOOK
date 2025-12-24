import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Module 1: ROS 2 Robotic Nervous System',
      items: [
        'module1/chapter1-nodes-topics',
        'module1/chapter2-services',
        'module1/chapter3-urdf-basics',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin',
      items: [
        'module2/chapter1-physics-simulation',
        'module2/chapter2-environment-building',
        'module2/chapter3-sensor-simulation',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac)',
      items: [
        'module3/chapter1-advanced-perception',
        'module3/chapter2-training-photorealistic-sim',
        'module3/chapter3-vslam-path-planning',
        'module3/chapter4-integration-and-workflow',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA)',
      items: [
        'module4/chapter1-llms-in-robotics',
        'module4/chapter2-voice-command-integration',
        'module4/chapter3-cognitive-planning-and-execution',
        'module4/chapter4-end-to-end-vla-workflow',
      ],
    },
  ],

  // But you can create a sidebar manually
  /*
  tutorialSidebar: [
    'intro',
    'hello',
    {
      type: 'category',
      label: 'Tutorial',
      items: ['tutorial-basics/create-a-document'],
    },
  ],
   */
};

export default sidebars;
