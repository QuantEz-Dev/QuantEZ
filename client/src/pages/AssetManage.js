import { Link } from "react-router-dom";
import React from "react";
import "../styles/AssetManage.scss";

const req = new Request('http://localhost:8000/assetmanagement/')

export const AssetManage = () => {
  return (
    <div className="assetManageWrap">
      <div className="assetManageTitle">
        <div className="assetManageTitleBox">
          <div className="boldTitle">
            <span>자산 입력하기</span>
          </div>
          <div className="subTitle">
            <span>자산을 입력하고 나의 투자 성향을 알아보세요!</span>
          </div>
        </div>
      </div>
      <form className="assetManageContent">
        <div className="assetManageContentBox">
          <div className="assetManageContentTitleBox">
            <div className="assetManageContentTitle">
              <span>제목</span>
              <input type="text" placeholder="제목을 입력하세요"></input>
            </div>
            <div className="assetManageContentSubTitle">
              <span>내용(선택)</span>
              <input type="text" placeholder="내용을 입력하세요"></input>
            </div>
          </div>
          <div className="assetManageInput">
            <div className="assetManageInputTop">
              <thead>
                <tr>
                  <th className="assetManageInputTHead">채권</th>
                  <th className="assetManageInputTHead">펀드</th>
                  <th className="assetManageInputTHead">ETF</th>
                  <th className="assetManageInputTHead">기타</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="assetManageInputTBody">
                    <input></input>
                    <label>원</label>
                  </td>
                  <td className="assetManageInputTBody">
                    <input></input>
                    <label>원</label>
                  </td>
                  <td className="assetManageInputTBody">
                    <input></input>
                    <label>원</label>
                  </td>
                  <td className="assetManageInputTBody">
                    <input></input>
                    <label>원</label>
                  </td>
                </tr>
              </tbody>
            </div>
          </div>
          <div className="assetManageInfo">
            <div className="assetManageInfoTitle">
              <span>도움말</span>
            </div>
            <div className="assetManageInfoContent">
              자신이 가진 자산을 입력해보세요!
              <br></br>
              안전자산과 위험자산으로 나누어 자신의 투자 유형을 분석해드립니다
              <br></br>
              <br></br>
              <b>안전 자산</b> : 손실의 위험이 적은 금융자산을 말합니다. 
              <br></br>
              <b>위험 자산</b>: 투자에 대한 수익률이 불확실한 투자자산을 말합니다.
              <br></br>
              <br></br>
              경제가 불확실성을 보일 땐 안전 자산, 경제가 호황일 땐 변동성이 크지만 큰 수익을 얻을 수 있는 위험 자산으로 투자가 몰라는 것이 일반적입니다.
            </div>
          </div>
          <div className="assetManageSubmitBtn">
            <button type="submit">
              <span>입력하기</span>
            </button>
          </div>
        </div>
      </form>
    </div>
    
  )
}