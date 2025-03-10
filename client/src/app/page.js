'use client';
import { useEffect } from "react";

export default function Home() {
  useEffect(() => {
    // Function to speak the welcome message
    const speakWelcome = () => {
      const message = "Welcome user! Click anywhere on the screen to initiate upload";
      const speech = new SpeechSynthesisUtterance(message);

      // Ensure speech is not interrupted
      speech.volume = 1; // Adjust volume if needed
      speech.rate = 1; // Adjust speech rate if needed
      speech.pitch = 1; // Adjust pitch if needed

      window.speechSynthesis.cancel(); // Stop any ongoing speech
      window.speechSynthesis.speak(speech);
    };

    // Use a small delay to bypass some browser restrictions
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
