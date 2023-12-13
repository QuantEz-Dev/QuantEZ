import React from "react";

export const DummyQuestion = () => {
  return (
    <div className="question-wrap">
      <div className="question-entire-title">
        질문과 답변
      </div>
      <div className="question-container">
        <div className="question-title">질문합니다</div>
        <div className="question-status">
          <div className="question-num">
            <span className="question-bold">번호</span>
            <span>1</span>
          </div>
          <div className="question-writer">
            <span className="question-bold">작성자</span>
            <span>jpaper</span>
          </div>
          <div className="question-date">
            <span className="question-bold">작성일</span>
            <span>2023.11.16</span>
          </div>
        </div>
        <div className="question-q-content">
          퀀트란 무엇인가요?
        </div>
      </div>
      <div className="answer-title">답변(1)</div>
      <div className="answer-wrap">
        <div className="answer-content">
          과거 투자 전문가의 감과 경험에 의존했던 투자를 벗어나서 수학적, 통계적, 공학적 기법을 동원하여 미래의 가치를 분석하고 수익을 창출하는 일을 담당하는 사람을 퀀트라고 합니다.

        </div>
        <div className="answer-writer">
            quantMaster
        </div>
      </div>
    </div>
  )

}