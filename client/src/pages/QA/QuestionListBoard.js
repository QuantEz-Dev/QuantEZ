import React, { useEffect, useState } from "react";
import "../../styles/QA.scss";
import axios from "axios";

// import CommonTable from "../../components/Table/Table";
// import CommonTableColumn from "../../components/Table/CommonTableColumn";
// import CommonTableRow from "../../components/Table/CommonTableRow";
import { Link } from "react-router-dom";
import { Question } from "./Question";

function QuestionListBoard() {
  const [questions, setQuestions] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/board/', {
      headers: {
        'Content-Type': 'application/json',
      },
    })
    .then((response) => {
      setQuestions(response.data);
      console.log(response.data);
    })
    .catch((error) => {
      console.error('Error fetching data: ', error);
    });
  }, []);


  return (
    <div className="qa-container">
      <div className="qa-wrap">
        <div className="qa-title">
          <span>질문과 답변</span>
        </div>
        <form>
          <div className="qalist-wrap">
            {/* TODO : 데이터 map 으로 받아오기 */}
            <div className="qalist-container">
              <div className="qalist-header qalist-flex">
                <div className="qalist-num">번호</div>
                <div className="qalist-title">제목</div>
                <div className="qalist-writer">글쓴이</div>
                <div className="qalist-date">날짜</div>
              </div>
              <div className="qalist-content qalist-flex">
                <div className="qalist-num">1</div>
                <Link className="qalist-title" style={{marginLeft: '1rem'}} to="/QA/1">
                  <div>질문합니다</div>
                </Link>
                <div className="qalist-writer">jpaper</div>
                <div className="qalist-date">2023.11.16</div>
              </div>
            </div>
          </div>
        </form>
        <button className="link-to-askquestion submit-btn" style={{marginBottom: '3rem'}}>
          <Link to={"/QA/AskQuestion"}>
            <span>작성하기</span>
          </Link>
        </button>
      </div>
    </div>
    
  )
}

export default QuestionListBoard;