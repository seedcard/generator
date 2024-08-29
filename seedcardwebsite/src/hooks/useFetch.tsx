import { useState, useEffect } from "react";
import axios from "axios";

const useFetchXpub = (url: any, password: any) => {
  const [loading, setLoading] = useState(false);
  const [xpub_qr, setXpub_qr] = useState("");
  const [err, setErr] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const res: any = await axios.get(url, {
          headers: {
            Authorization: `${password}`,
          },
        });
        setXpub_qr(res);
      } catch (err: any) {
        setErr(err);
      }
      setLoading(false);
    };
    fetchData();
  }, [url]);

  return { loading, xpub_qr, err };
};

const useFetchNewallet = (url: any, password: any) => {
  const [data, setData] = useState({});
  const [wallet_loading, setWalletLoading] = useState(false);
  const [err, setErr] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      setWalletLoading(true);
      try {
        const res: any = await axios.get(url, {
          headers: {
            Authorization: `${password}`,
          },
        });
        setData(res);
      } catch (err: any) {
        setErr(err);
      }
      setWalletLoading(false);
    };
    fetchData();
  }, [url]);

  return { wallet_loading, data, err };
};

const useFetchRandomise = (url: any, password: any) => {
  const [msg, setMsg] = useState("");
  const [r_loading, setRLoading] = useState(false);
  const [err, setErr] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      setRLoading(true);
      try {
        const res: any = await axios.get(url, {
          headers: {
            Authorization: `${password}`,
          },
        });
        setMsg(res);
      } catch (err: any) {
        setErr(err);
      }
      setRLoading(false);
    };
    fetchData();
  }, [url]);

  return { msg, r_loading, err };
};

const useFetchGenerateWalletQr = (url: any, password: any) => {
  const [wallet_qr, setWalletQr] = useState("");
  const [qr_loading, setQrLoading] = useState(false);
  const [err, setErr] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      setQrLoading(true);
      try {
        const res: any = await axios.get(url, {
          headers: {
            Authorization: `${password}`,
          },
        });
        setWalletQr(res);
      } catch (err: any) {
        setErr(err);
      }
      setQrLoading(false);
    };
    fetchData();
  }, [url]);

  return { wallet_qr, qr_loading, err };
};

export {
  useFetchXpub,
  useFetchNewallet,
  useFetchRandomise,
  useFetchGenerateWalletQr,
};
