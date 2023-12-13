// import { useState } from "react";
import { Link } from "react-router-dom";
import { ReactComponent as Mainlogo } from "../assets/img/Mainlogo.svg";
export const Navbar = () => {
  // const [value, setValue] = useState("");
  return (
    <div id="header">
      <div id="header-top">
        <div id="header-top-right">
          <ul>
            <li>
              <Link to="/login">로그인</Link>
              <span>&nbsp;&nbsp; | &nbsp;&nbsp;</span>
            </li>
            <li>
              <Link class="login" to="/Mypage">
                마이페이지
              </Link>
              <span>&nbsp;&nbsp; | &nbsp;&nbsp;</span>
            </li>
            <li>
              <Link class="login" to="/QA">
                질문게시판
              </Link>
              <span>&nbsp;&nbsp; | &nbsp;&nbsp;</span>
            </li>
            <li class="in-select">
              <select
                onChange={(event) =>
                  event.target.value
                    ? window.open(event.target.value, "_blank")
                    : ""
                }
              >
                <option value="">연관 사이트</option>
                <option value="https://www.samsungpop.com/">삼성증권</option>
                <option value="https://www.nhqv.com/">NH증권</option>
                <option value="https://securities.koreainvestment.com/main/Main.jsp">
                  한국투자증권
                </option>
              </select>
            </li>
          </ul>
        </div>
      </div>
      <div id="header-con">
        <Link to="/">
          <Mainlogo />
        </Link>
        <nav id="gnb">
          <ul>
            <li class="gnb-depth-1">
              <Link className="gnb-depth-1-btn" to="/assetManage">
                {" "}
                자산관리
              </Link>
            </li>
            <li class="gnb-depth-1">
              <Link class="gnb-depth-1-btn" to="/financeSheetlist">
                {" "}
                재무제표학습
              </Link>
            </li>
            <li class="gnb-depth-1">
              {" "}
              <li class="gnb-depth-1-btn">
                백테스트
                <li class="gnb-depth-2">
                  <li>
                     <Link class="gnb-depth-2-btn" to="/tutorial">
                      튜토리얼
                     </Link>
                  </li>
                  <li>
                    <Link to="/port">
                      포트 만들기
                    </Link>
                  </li>
                </li>
              </li>
            </li>
            <li class="gnb-depth-1">
              <Link class="gnb-depth-1-btn" to="/aboutus">
                퀀티지란?
              </Link>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  );
};
