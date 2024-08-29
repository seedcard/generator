import { Navbar } from "../../Components";
import "./style.scss";
import { useState } from "react";
import { useWalletContext } from "../../Context/walletContext";

function Homepage() {
  const [password, setPassword] = useState("");
  const [walletName, setWalletName] = useState("");
  const [cardissuer, setCardIssuer] = useState("");
  const url: any = "https://walletqrgenerator.onrender.com";
  const {
    wallet_qr,
    xpub_qr,
    words,
    data,
    msg,
    hidden_words,
    useFetchXpub,
    useFetchNewallet,
    useFetchRandomise,
    useFetchGenerateWalletQr,
  } = useWalletContext();

  const handleReload = () => {
    window.location.reload();
  };

  const Getxpub = async () => {
    if (password == "" || cardissuer.length == 0)
      return alert("Password is required");
    await useFetchXpub(`${url}/xpub`, password);
  };
  const GenerateSeed = async () => {
    if (password == "" || cardissuer.length == 0)
      return alert("Password is required");
    await useFetchNewallet(`${url}/generatewallet`, password, words);
    console.log(data);
  };
  const Generateqr = async () => {
    if (password == "" || walletName.length != 16 || cardissuer.length == 0)
      return alert(
        "Password is required or wallet name should be 16 characters"
      );
    await useFetchGenerateWalletQr(
      `${url}/walletname_qr`,
      password,
      walletName
    );
  };

  const GetRandomise = async () => {
    if (password == "" || cardissuer.length == 0)
      return alert("Password is required");
    await useFetchRandomise(`${url}/randomise`, password, words);
  };

  return (
    <div className="_homepage bg-black pb-10">
      <Navbar />
      <main className="main pt-10">
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-4 _card_flex">
            <h1 className="text-white">ENTER CARD ISSUER</h1>
            <input
              onChange={(e) => setCardIssuer(e.target.value)}
              type="text"
              className="px-3 py-2 outline-none _card_iss"
              placeholder="XX"
            />
          </div>
          <div className="flex items-center gap-4 _card_flex">
            <h1 className="text-white">ENTER PASSWORD</h1>
            <input
              required
              type="text"
              placeholder="XXXXXX"
              onChange={(e) => setPassword(e.target.value)}
              className="px-3 py-2 outline-none _card_iss"
            />
          </div>
        </div>
        {/* XPUBQR */}
        <div className="flex justify-between items-center mt-14">
          <h1>GENERATE XPUB QR</h1>
          <div className="flex items-center gap-10 _qr_flex">
            <button onClick={Getxpub}>
              <div className="h-10 w-10 rounded-full bg-green-500"></div>
            </button>
            <div
              style={{ width: "150px", height: "150px" }}
              className="bg-white"
            >
              <img
                src={`${
                  xpub_qr == "" || undefined
                    ? "qr.png"
                    : `data:image/png;base64,${xpub_qr}`
                }`}
                alt="qr.png"
                className="h-full w-full"
              />
            </div>
          </div>
        </div>

        {/* SEEDQR */}
        <div className="flex justify-between items-center mt-8">
          <h1>GENERATE SEEDQR</h1>
          <div className="flex items-center gap-10 _qr_flex">
            <button onClick={GenerateSeed}>
              <div className="h-10 w-10 rounded-full bg-green-500"></div>
            </button>
            <div
              style={{ width: "150px", height: "150px" }}
              className="bg-white"
            >
              <img
                src={`${
                  data == "" || undefined
                    ? "qr.png"
                    : `data:image/png;base64,${data.img_newallet}`
                }`}
                alt="qr.png"
                className="h-full w-full"
              />
            </div>
          </div>
        </div>

        {/* WALLET NAME */}
        <div className="flex items-center justify-between mt-8 _wallet_nme">
          <h1 className="text-white">ENTER WALLET NAME</h1>
          <input
            type="text"
            placeholder="XX04A6787A4F1390"
            onChange={(e) => setWalletName(e.target.value)}
            className="px-3 py-2 outline-none _wallet_name"
          />
        </div>
        {/* GENERATE WALLETQR */}
        <div className="flex justify-between items-center mt-8">
          <h1>GENERATE WALLET NAME QR</h1>
          <div className="flex items-center gap-10 _qr_flex">
            <button onClick={Generateqr}>
              <div className="h-10 w-10 rounded-full bg-green-500"></div>
            </button>
            <div
              style={{ width: "150px", height: "150px" }}
              className="bg-white"
            >
              <img
                src={`${
                  wallet_qr == "" || undefined
                    ? "qr.png"
                    : `data:image/png;base64,${wallet_qr}`
                }`}
                alt="qr.png"
                className="h-full w-full"
              />
            </div>
          </div>
        </div>

        {/* FINGERPRINT DISPLAY CONTAINER */}
        <div className="flex justify-between items-center mt-6">
          <div className="flex flex-col gap-4 items-center justify-center">
            <input
              value={`${
                !data.fingerprint1 || undefined ? "" : `${data.fingerprint1}`
              }`}
              type="text"
              className="px-3 py-4 outline-none _card_iss"
              placeholder=""
            />
            <h1>FINGERPRINT 1</h1>
          </div>
          <div className="flex flex-col gap-4 items-center justify-center">
            <input
              value={`${
                !data.fingerprint2 || undefined ? "" : `${data.fingerprint2}`
              }`}
              type="text"
              className="px-3 py-4 outline-none _card_iss"
              placeholder=""
            />
            <h1>FINGERPRINT 2</h1>
          </div>
        </div>

        {/* RANDOMISATION */}
        <div className="flex justify-between items-center mt-8">
          <h1>RANDOMISATION</h1>
          <div className="flex items-center gap-10 _qr_flex">
            <button onClick={GetRandomise}>
              <div className="h-10 w-10 rounded-full bg-green-500"></div>
            </button>
            <input
              type="text"
              value={`${msg == "" || undefined ? "" : `${msg}`}`}
              className="px-3 py-2 outline-none _wallet_name"
              placeholder="3 / 11 / 12 / 2 / 1 / 10"
            />
          </div>
        </div>

        {/* RETURN MESSAGE */}
        <div className="mt-16 flex flex-col gap-6 items-center justify-center">
          <input
                      type="text"
                      value={`${!data.fingerprint1 || cardissuer == "" || hidden_words == "" ? "" : data.fingerprint1+"_"+cardissuer+"_"+hidden_words}`}
            className="w-full p-4"
            placeholder=" 39a103a7_MM_ decembermotheropenarchoxygeneternal
"
          />
          <h1>OP_RETURN MESSAGE</h1>
        </div>

        {/* RESTART BUTTON BOTTOM */}
        <div className="mt-20 flex flex-col gap-6 justify-center items-center">
          <button onClick={handleReload}>
            <div className="h-10 w-10 rounded-full bg-green-500"></div>
          </button>
          <h1>RESTART</h1>
        </div>
      </main>
    </div>
  );
}

export default Homepage;
