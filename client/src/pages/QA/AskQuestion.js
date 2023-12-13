import React, {useEffect, useRef, useState} from "react";
import ReactQuill from "react-quill";
import 'react-quill/dist/quill.snow.css';
import "../../styles/QA.scss";
import axios from "axios";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";

export const AskQuestion = () => {
  const navigate = useNavigate();
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");

  const handleTitleChange = (e) => {
    setTitle(e.target.value);
  };
  const handleContentChange = (value) => {
    setContent(value);
  }

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await axios.post('http://127.0.0.1:8000/board/question/create/', {
        subject: title,
        content: content,
      });

      if (response.status === 201) {
        alert('성공적으로 질문이 등록되었습니다.');
        navigate('/QA');
      } else {
        console.error('Failed to post question', response);
      }
    } catch (error) {
      console.error('Failed to post question: ', error);
    }
  };

  return (
    <div className="qa-container">
      <div className="qa-wrap">
        <div className="qa-title">
          <span>질문 등록하기</span>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="qa-user-input">
            <div className="qa-user-title">
              <dl>
                <dt>제목</dt>
                <dd>
                  <input className="user-title-input" type="text" placeholder="제목 입력" value={title} onChange={handleTitleChange}></input>
                </dd>
              </dl>
            </div>
            <ReactQuill style={{height: '40rem'}} value={content} onChange={handleContentChange}></ReactQuill>
          </div>
          <button  type="submit" className="submit-btn">
            등록하기
          </button>
        </form>
      </div>
    </div>
  )
}
