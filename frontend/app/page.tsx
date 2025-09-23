import Header from "./components/header";
import CustomChatSection from "./components/chat-section";

export default function Home() {
  return (
    <main className="h-screen w-screen flex justify-center items-center background-gradient">
      <div className="space-y-2 lg:space-y-6 w-[90%] lg:w-[60rem] pt-4">
        <Header />
        <div className="h-[85vh] flex">
          <CustomChatSection />
        </div>
      </div>
    </main>
  );
}
