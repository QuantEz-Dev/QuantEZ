import { Link } from "react-router-dom";
import userPic from "../assets/img/portrait_placeholder.png";
import React from "react";
import { Chart as ChartJS, ArcElement, Tooltip } from 'chart.js';
import { Pie } from 'react-chartjs-2';
import "../styles/MyPage.css";

ChartJS.register(ArcElement, Tooltip);

function get_data() {
  fetch('http://127.0.0.1:8000/')
  .then((response) => response.json())
  .then((data) => console.log((data)));
}

export const data = {
  responsive: false, 
  labels: ['채권', '펀드', 'ETF', 'etc'],
  datasets: [
    {
      data: [30, 20, 10, 40],
      backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(153, 102, 255, 0.2)',
      ],
      borderColor: [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(153, 102, 255, 1)',
      ],
      borderWidth: 1,
    },
  ],
};

export const MyPage = () => {
  return (
    <div className="wrap">
      <div className="myPageBox">
        <div className="userInfo">
          <div className="userimgBox">
            <img src={userPic} alt="user_img"></img>
          </div>
          <div className="username">
            <p><b className="bold">임정희</b>님, 안녕하세요!</p>
          </div>
        </div>

        <div className="userContentBox">
          <div className="portViewTitle">
            나의 투자유형
          </div>
          <div className="portChart">
            <Pie data={data} />
          </div>
          <div className="portTable">
            <table>
              <thead>
                <tr>
                  <th>종목</th>
                  <th>자산</th>
                  <th>비율(%)</th>
                </tr>
              </thead>
              <tbody>
                <tr className="bond">
                  <td>채권</td>
                  <td></td>
                  <td>30</td>
                </tr>
                <tr className="fund">
                  <td>펀드</td>
                  <td></td>
                  <td>20</td>
                </tr>
                <tr className="ETF">
                  <td>ETF</td>
                  <td></td>
                  <td>10</td>
                </tr>
                <tr className="Etc">
                  <td>기타</td>
                  <td></td>
                  <td>40</td>
                </tr>
              </tbody>
            </table>
          </div>

          <form className="portModify">
            <button className="portModifyButton">
              수정하기
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};