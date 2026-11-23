// A Random Tuesday as a flat 2D scrapbook. Remotion draws the pictures only; pipeline/edit.py adds captions, hook, sound.
import React from "react";
import {AbsoluteFill, Composition, interpolate, registerRoot, spring, useCurrentFrame, useVideoConfig} from "remotion";
import "@fontsource/caveat/700.css";
import durations from "../../stories/random-tuesday-2d/durations.json";

const FPS = 30;
const D = durations as Record<string, number>;
const SHOTS = Object.keys(D);
const START: Record<string, number> = {};
let acc = 0;
for (const s of SHOTS) { START[s] = Math.round(acc * FPS); acc += D[s]; }
export const TOTAL = Math.round(acc * FPS);
const LABEL: Record<string, string> = {r1: "7:42 am", r2: "7:58 am", r3: "8:20 am", r4: "4:05 pm", r5: "6:31 pm", r6: "7:10 pm", r7: "9:47 pm"};
const TILT: Record<string, number> = {r1: -4, r2: 3, r3: -2, r4: 5, r5: -5, r6: 2, r7: 0};
const INK = "#3b2f2a";
const SKIN = "#f2c29b";

// ---------------------------------------------------------------- flat people (one look for the whole family)
const Person: React.FC<{x: number; y: number; s?: number; top: string; hair: string; bun?: boolean; beard?: boolean;
  glasses?: boolean; mouth?: "smile" | "o" | "flat"; arm?: number}> = ({x, y, s = 1, top, hair, bun, beard, glasses, mouth = "smile", arm = 0}) => (
  <g transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-58} y={40} width={116} height={150} rx={50} fill={top} />
    <rect x={-80} y={60} width={26} height={90} rx={13} fill={top} transform={`rotate(${arm} -67 66)`} />
    <rect x={54} y={60} width={26} height={90} rx={13} fill={top} />
    <circle cx={0} cy={0} r={52} fill={SKIN} />
    <path d="M -54 -6 Q -50 -62 0 -60 Q 50 -62 54 -6 Q 30 -36 0 -34 Q -30 -36 -54 -6 Z" fill={hair} />
    {bun && <circle cx={0} cy={-64} r={20} fill={hair} />}
    {beard && <path d="M -40 14 Q 0 64 40 14 Q 20 30 0 30 Q -20 30 -40 14 Z" fill={hair} />}
    <circle cx={-18} cy={2} r={6} fill={INK} /><circle cx={18} cy={2} r={6} fill={INK} />
    {glasses && <g fill="none" stroke={INK} strokeWidth={4}><circle cx={-18} cy={2} r={14} /><circle cx={18} cy={2} r={14} /><path d="M -4 2 H 4" /></g>}
    {mouth === "smile" && <path d="M -14 22 Q 0 34 14 22" stroke={INK} strokeWidth={5} fill="none" strokeLinecap="round" />}
    {mouth === "o" && <ellipse cx={0} cy={26} rx={10} ry={13} fill={INK} />}
    {mouth === "flat" && <path d="M -12 26 H 12" stroke={INK} strokeWidth={5} strokeLinecap="round" />}
    <circle cx={-32} cy={18} r={8} fill="#ef9a8a" opacity={0.6} /><circle cx={32} cy={18} r={8} fill="#ef9a8a" opacity={0.6} />
  </g>
);
const KID = {top: "#f4c430", hair: "#6b4226"};
const MUM = {top: "#5c9e6e", hair: "#8a4b2a", bun: true};
const DAD = {top: "#3f6fb5", hair: "#4a3424", beard: true};
const SIS = {top: "#d8433b", hair: "#2f2320"};
const GRAN = {top: "#8a5fa8", hair: "#cfcfcf", glasses: true, bun: true};

// ---------------------------------------------------------------- one illustration per moment (680 x 640, f = frame inside the shot)
const Pic: React.FC<{shot: string; f: number}> = ({shot, f}) => {
  const t = f / FPS;
  const wob = Math.sin(t * 6);
  switch (shot) {
    case "r1": return (<g>
      <rect width={680} height={640} fill="#fbe3b8" />
      <rect x={300} y={70} width={300} height={260} rx={10} fill="#bfe3f5" stroke="#fff" strokeWidth={16} />
      <circle cx={520} cy={150 - t * 6} r={40} fill="#ffd25e" />
      <rect x={0} y={470} width={680} height={170} fill="#e0a96d" />
      <Person x={240} y={300 + wob * 2} {...KID} arm={-30} />
      <path d="M 185 430 Q 240 470 295 430 Z" fill="#fff" stroke={INK} strokeWidth={4} />
      {[0, 1, 2].map((i) => <circle key={i} cx={215 + i * 25} cy={428 - Math.abs(Math.sin(t * 4 + i)) * 6} r={9} fill="#f0b43c" />)}
    </g>);
    case "r2": {
      const pop = interpolate(f, [10, 16, 24], [0, -150, -120], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
      return (<g>
        <rect width={680} height={640} fill="#d9ecdf" />
        <rect x={0} y={430} width={680} height={210} fill="#b98a5e" />
        <rect x={210 + 40} y={250 + pop} width={70} height={90} rx={14} fill="#2b211c" />
        <rect x={320 + 40} y={250 + pop} width={70} height={90} rx={14} fill="#2b211c" />
        <rect x={210} y={300} width={260} height={150} rx={40} fill="#c9ced6" stroke={INK} strokeWidth={5} />
        {[0, 1, 2].map((i) => <circle key={i} cx={300 + i * 50 + Math.sin(t * 3 + i) * 12} cy={180 + pop * 0.6 - ((t * 60 + i * 40) % 140)}
          r={26 + i * 6} fill="#8c8c8c" opacity={interpolate(f, [14, 30], [0, 0.6], {extrapolateLeft: "clamp", extrapolateRight: "clamp"})} />)}
        <Person x={560} y={330} s={0.9} {...MUM} mouth="o" arm={-150} />
      </g>);
    }
    case "r3": return (<g>
      <rect width={680} height={640} fill="#cfe0f2" />
      <rect x={30} y={60} width={620} height={300} rx={40} fill="#e9f4fb" stroke="#9fb6c9" strokeWidth={14} />
      <rect x={0} y={420} width={680} height={220} fill="#55606e" />
      <Person x={230} y={330 + wob * 6} {...DAD} mouth="o" arm={-40} />
      <Person x={470} y={350} s={0.85} {...KID} mouth="flat" />
      {[0, 1, 2].map((i) => <text key={i} x={300 + i * 60 + Math.sin(t * 2 + i) * 20} y={260 - ((t * 90 + i * 60) % 200)} fontSize={60} fill={INK}>♪</text>)}
      <circle cx={230} cy={500} r={70} fill="none" stroke="#2b2b2b" strokeWidth={18} />
    </g>);
    case "r4": {
      const x = interpolate(f, [0, 50], [-120, 820]);
      return (<g>
        <rect width={680} height={640} fill="#f6dcd6" />
        <rect x={0} y={470} width={680} height={170} fill="#c78f66" />
        {[0, 1, 2].map((i) => <path key={i} d={`M ${x - 120 - i * 30} ${260 + i * 50} h -90`} stroke={INK} strokeWidth={6} strokeLinecap="round" opacity={0.5} />)}
        <Person x={x} y={300 + Math.abs(Math.sin(t * 14)) * -20} {...SIS} arm={-60} />
        <Person x={140} y={320} s={0.8} {...KID} top="#f2efe7" mouth="o" />
      </g>);
    }
    case "r5": return (<g>
      <rect width={680} height={640} fill="#efe0f5" />
      <rect x={180} y={60} width={320} height={540} rx={50} fill="#2b2b2b" />
      <rect x={200} y={110} width={280} height={440} rx={20} fill="#fff7e8" />
      <Person x={340} y={300} s={0.9} {...GRAN} />
      <text x={340} y={500} fontSize={44} textAnchor="middle" fill={INK} fontFamily="Caveat">Grandma ♥</text>
      {[0, 1, 2].map((i) => <circle key={i} cx={340} cy={330} r={190 + ((t * 120 + i * 60) % 180)} fill="none" stroke="#c9a3df"
        strokeWidth={6} opacity={1 - ((t * 120 + i * 60) % 180) / 180} />)}
    </g>);
    case "r6": return (<g>
      <rect width={680} height={640} fill="#e3e6ea" />
      <rect x={60} y={380} width={560} height={160} rx={50} fill="#7b8fa6" />
      <rect x={60} y={330} width={120} height={210} rx={50} fill="#6a7e95" />
      <g transform="rotate(-90 360 400)"><Person x={360} y={400} s={0.85} {...KID} mouth="flat" /></g>
      <text x={430} y={250} fontSize={90} fill={INK} fontFamily="Caveat" opacity={(Math.floor(t * 2) % 2) ? 1 : 0.4}>…</text>
    </g>);
    default: return (<g>
      <rect width={680} height={640} fill="#3a2f45" />
      <rect x={140} y={70} width={400} height={230} rx={16} fill="#9fd3ff" opacity={0.85 + Math.sin(t * 5) * 0.1} />
      <ellipse cx={340} cy={380} rx={330} ry={210} fill="#ffcf8a" opacity={0.25 + Math.sin(t * 5) * 0.05} />
      <rect x={20} y={430} width={640} height={190} rx={60} fill="#b5654a" />
      <Person x={110} y={430} s={0.62} {...GRAN} />
      <Person x={230} y={410} s={0.72} {...DAD} />
      <Person x={350} y={430} s={0.62} {...KID} />
      <Person x={460} y={420} s={0.68} {...MUM} />
      <Person x={575} y={435} s={0.6} {...SIS} />
    </g>);
  }
};

// ---------------------------------------------------------------- the scrapbook page
const Card: React.FC<{shot: string; f: number; x: number; y: number; rot: number; scale: number; dim?: number}> = ({shot, f, x, y, rot, scale, dim = 0}) => (
  <div style={{position: "absolute", left: x - 380, top: y - 440, width: 760, height: 880, transform: `rotate(${rot}deg) scale(${scale})`,
    background: "#fffdf8", boxShadow: "0 18px 40px rgba(60,40,20,0.28)", padding: 40, boxSizing: "border-box", filter: `brightness(${1 - dim})`}}>
    <svg width={680} height={640} viewBox="0 0 680 640" style={{display: "block"}}><Pic shot={shot} f={f} /></svg>
    <div style={{fontFamily: "Caveat", fontSize: 92, color: INK, textAlign: "center", marginTop: 26}}>Tue · {LABEL[shot]}</div>
    <div style={{position: "absolute", left: 270, top: -30, width: 220, height: 64, background: "rgba(245,214,120,0.75)", transform: "rotate(-3deg)"}} />
  </div>
);

const Page: React.FC = () => {
  const frame = useCurrentFrame(); const {fps} = useVideoConfig();
  const idx = Math.max(0, SHOTS.filter((s) => START[s] <= frame).length - 1);
  const shot = SHOTS[idx]; const f = frame - START[shot];
  const final = shot === "r7";
  const drop = spring({frame: f, fps, config: {damping: 13, mass: 0.8}});
  const fan = final ? spring({frame: f, fps, config: {damping: 16}}) : 0;
  const under = SHOTS.slice(0, idx);
  const spots = [[250, 360, -12], [830, 380, 10], [230, 1440, 8], [850, 1460, -9], [180, 900, -6], [900, 920, 7]];
  return (
    <AbsoluteFill style={{background: "#f1e6d2"}}>
      <svg width={1080} height={1920} style={{position: "absolute"}}>
        <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} /><feColorMatrix values="0 0 0 0 0.45  0 0 0 0 0.35  0 0 0 0 0.25  0 0 0 0.08 0" /></filter>
        <rect width={1080} height={1920} filter="url(#grain)" />
        {Array.from({length: 24}).map((_, i) => <line key={i} x1={0} x2={1080} y1={120 + i * 76} y2={120 + i * 76} stroke="#d9c7a8" strokeWidth={2} />)}
      </svg>
      {under.map((s, i) => {
        const [fx, fy, fr] = spots[i % spots.length];
        const back = under.length - i;                       // older cards sit lower in the pile
        const px = 540 + back * 14 * (i % 2 ? 1 : -1), py = 820 + back * 18;
        return <Card key={s} shot={s} f={Math.round(D[s] * FPS)} x={interpolate(fan, [0, 1], [px, fx])} y={interpolate(fan, [0, 1], [py, fy])}
          rot={interpolate(fan, [0, 1], [TILT[s], fr])} scale={interpolate(fan, [0, 1], [0.86, 0.42])} dim={final ? 0 : Math.min(0.35, back * 0.08)} />;
      })}
      <Card shot={shot} f={f} x={540} y={interpolate(drop, [0, 1], [-700, 800])} rot={interpolate(drop, [0, 1], [TILT[shot] - 14, TILT[shot]])}
        scale={final ? interpolate(fan, [0, 1], [0.92, 0.8]) : 0.92} />
    </AbsoluteFill>
  );
};

registerRoot(() => <Composition id="RandomTuesday" component={Page} durationInFrames={TOTAL} fps={FPS} width={1080} height={1920} />);
