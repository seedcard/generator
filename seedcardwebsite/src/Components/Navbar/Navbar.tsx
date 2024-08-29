import { seed } from "../../assets";
import "./style.scss";

function Navbar() {
  return (
    <div>
      <div className="_navbar_container">
        <div className="flex justify-between items-center py-6">
          <img src={seed} alt="logo.png" className="h-14 w-auto" />
          <h1 className="text-white">WALLET GENERATOR v1.0</h1>
        </div>
      </div>
      <hr />
    </div>
  );
}

export default Navbar;
