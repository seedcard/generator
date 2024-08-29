import { Homepage } from "./Pages"
import "./App.css"
import { WalletProvider } from "./Context/walletContext"

function App() {

  return (
    <WalletProvider>
      <>
        <Homepage />
      </>
    </WalletProvider>
  );
}

export default App
