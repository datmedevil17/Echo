'use client';
import { useEffect } from "react";

export default function Home() {
  useEffect(() => {
    const speakWelcome = () => {
      const message = "Welcome user! Click anywhere on the screen to initiate upload";
      const speech = new SpeechSynthesisUtterance(message);
      speech.volume = 100;
      speech.rate = 1;
      speech.pitch = 1;
      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(speech);
    };

    setTimeout(speakWelcome, 500);
  }, []);

  return (
    <div 
      className="min-h-screen flex flex-col items-center justify-center p-4 cursor-pointer"
      onClick={() => {
        console.log("Upload initiated");
      }}
    >
      <h1 className="text-2xl font-bold mb-4">Welcome to Echo</h1>
      <p className="text-gray-600">Click anywhere on the screen to initiate upload</p>
    </div>
  );
}