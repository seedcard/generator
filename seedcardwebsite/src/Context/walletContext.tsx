import { createContext, useContext, useState } from "react";
import axios from "axios";

interface Props {
  children: React.ReactNode;
}
interface WalletContextType {
  loading: boolean;
  err: boolean;
  wallet_qr: string;
  xpub_qr: string;
  words: string[];
  data: any; // Adjust type based on expected data
  msg: string;
  hidden_words: string;
  useFetchXpub: (url: string, password: string) => Promise<string>;
  useFetchNewallet: (url: string, password: string) => Promise<any>; // Adjust the type as needed
  useFetchRandomise: (url: string, password: string) => Promise<string>;
  useFetchGenerateWalletQr: (url: string, password: string) => Promise<string>;
  // Add other properties here as needed
}
// const WalletContext = createContext<WalletContextType | null>(null);
// Define the context
const walletContext = createContext<WalletContextType | any>(null);

// Context Provider Component
export const WalletProvider: React.FC<Props> = ({ children }) => {
  // Shared states for all requests
  const [loading, setLoading] = useState<boolean>(false);
  const [err, setErr] = useState<string | boolean>(false);
  const [wallet_qr, setWalletQr] = useState<string>("");
  const [xpub_qr, setXpub_qr] = useState<string>("");
  const [words, setWords] = useState<string>("");
  const [data, setData] = useState<Record<string, any>>({});
  const [msg, setMsg] = useState<string>("");
  const [hidden_words, setHiddenWords] = useState<string>("");

  const useFetchXpub = async (url: string, password: string) => {
    // const [xpub_qr, setXpub_qr] = useState("");
    setLoading(true);
    try {
      const res: any = await axios.get(url, {
        headers: {
          Authorization: `${password}`,
          "Content-Type": "application/json",
        },
      });
      console.log(res);
      setXpub_qr(res.data.img_xpub);
      setWords(res.data.words);
    } catch (error) {
      setErr(true);
    }
    setLoading(false);
    return xpub_qr;
  };

  const useFetchNewallet = async (
    url: string,
    password: string,
    words: string[]
  ) => {
    // const [data, setData] = useState({});
    setLoading(true);
    try {
      const datax: any = {
        words: words,
      };
      const res = await axios.post(url, datax, {
        headers: {
          Authorization: `${password}`,
          "Content-Type": "application/json",
        },
      });
      setData(res.data);
    } catch (error) {
      setErr(true);
    }
    setLoading(false);
    return data;
  };

  const useFetchRandomise = async (
    url: string,
    password: string,
    words: string[]
  ) => {
    // const [msg, setMsg] = useState("");
    setLoading(true);
    try {
      const data: any = {
        words: words,
      };
      const res = await axios.post(url, data, {
        headers: {
          Authorization: `${password}`,
        },
      });
      setMsg(res.data.msg);
      setHiddenWords(res.data.hidden_words);
    } catch (error) {
      setErr(true);
    }
    setLoading(false);
  };

  const useFetchGenerateWalletQr = async (
    url: string,
    password: string,
    wallet_name: string
  ) => {
    // const [wallet_qr, setWalletQr] = useState("");
    setLoading(true);
    try {
      const data: any = {
        wallet_name: wallet_name,
      };
      const res = await axios.post(url, data, {
        headers: {
          Authorization: `${password}`,
          "Content-Type": "application/json",
        },
      });
      setWalletQr(res.data.img_walletnme);
    } catch (error) {
      setErr(true);
    }
    setLoading(false);
    // return wallet_qr;
  };

  return (
    <walletContext.Provider
      value={{
        loading,
        err,
        wallet_qr,
        xpub_qr,
        data,
        msg,
        words,
        hidden_words,
        useFetchXpub,
        useFetchNewallet,
        useFetchRandomise,
        useFetchGenerateWalletQr,
      }}
    >
      {children}
    </walletContext.Provider>
  );
};

// Custom hook to use the context
export const useWalletContext = () => useContext(walletContext);
// export const useWalletContext = () => {
//   const context = useContext(WalletContext);
//   if (!context) {
//     throw new Error("useWalletContext must be used within a WalletProvider");
//   }
//   return context;
// };
