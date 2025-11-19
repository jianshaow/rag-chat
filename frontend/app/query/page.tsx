import Home from "./Home";
import { ConfigProvider } from "../context/ConfigContext";

export default function Page() {
  return (
    <ConfigProvider>
      <Home />
    </ConfigProvider>
  );
}