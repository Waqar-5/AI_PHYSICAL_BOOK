// import type {ReactNode} from 'react';
// import clsx from 'clsx';
// import Heading from '@theme/Heading';
// import styles from './styles.module.css';

// type FeatureItem = {
//   title: string;
//   Svg: React.ComponentType<React.ComponentProps<'svg'>>;
//   description: ReactNode;
// };

// const FeatureList: FeatureItem[] = [
//   {
//     title: 'The First Truly Alive Textbook',
//     Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default,
//     description: (
//       <>
//         Ask questions about any paragraph · Get instant personalized explanations based on your background · Switch to Urdu with one click · All inside the book, no page reloads.  
//         This isn’t a static PDF — it’s your AI co-teacher for Physical AI & Humanoid Robotics.
//       </>
//     ),
//   },
//   {
//     title: 'From Voice Command to Real Humanoid',
//     Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default,
//     description: (
//       <>
//         Every chapter includes ready-to-run ROS 2 code, URDFs, Gazebo worlds, and NVIDIA Isaac Sim scenes.  
//         Go from reading to controlling a real Unitree G1 humanoid in the same day.
//       </>
//     ),
//   },
//   {
//     title: 'Master the Full Physical AI Stack',
//     Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
//     description: (
//       <>
//         ROS 2 → Gazebo & Unity → NVIDIA Isaac → Vision-Language-Action (VLA) models.  
//         The complete capstone journey to build autonomous humanoids that understand physics and natural language.
//       </>
//     ),
//   },
// ];

// function Feature({title, Svg, description}: FeatureItem) {
//   return (
//     <div className={clsx('col col--4')}>
//       <div className="text--center">
//         <Svg className={styles.featureSvg} role="img" />
//       </div>
//       <div className="text--center padding-horiz--md">
//         <Heading as="h3">{title}</Heading>
//         <p>{description}</p>
//       </div>
//     </div>
//   );
// }

// export default function HomepageFeatures(): ReactNode {
//   return (
//     <section className={styles.features}>
//       <div className="container">
//         <div className="row">
//           {FeatureList.map((props, idx) => (
//             <Feature key={idx} {...props} />
//           ))}
//         </div>
//       </div>
//     </section>
//   );
// }


import type { ReactNode } from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'The First Truly Alive Textbook',
    Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        Ask any question · Get <strong className="text-purple-400">personalized answers</strong> · Switch to Urdu instantly · All inside the book
        <br /><br />
        <span className="text-pink-300 font-bold">This isn’t a PDF — it’s your AI co-teacher</span>
      </>
    ),
  },
  {
    title: 'From Voice to Real Humanoid',
    Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
      Ready-to-run ROS 2 · URDFs · Gazebo · Isaac Sim · Unitree G1 · Nav2 · VSLAM · rclpy · Depth Cameras · IMU Sensors
        <br /><br />
        <span className="text-cyan-300 font-bold">Control a real humanoid robot — today</span>
      </>
    ),
  },
  {
    title: 'Master Physical AI End-to-End',
    Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        ROS 2 → Digital Twin → NVIDIA Isaac → Vision-Language-Action
        <br /><br />
        <span className="text-emerald-300 font-bold">Build autonomous humanoids that understand physics & language</span>
      </>
    ),
  },
];

function Feature({ title, Svg, description }: FeatureItem) {
  return (
    <div className={clsx('col col--4', styles.featureCard)}>
      <div className={styles.cardInner}>
        <div className={styles.svgContainer}>
          <Svg className={styles.featureSvg} role="img" />
        </div>
        <div className={styles.content}>
          <Heading as="h3" className={styles.title}>{title}</Heading>
          <p className={styles.description}>{description}</p>
        </div>
        <div className={styles.shine} />
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}