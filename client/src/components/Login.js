import React, { useState } from "react";
import * as S from "../styles/Login.styled";
import Axios from "axios";
import axios from "axios";

export const Login = () => {
  const [signIn, toggle] = useState(true);

  const [name, setUserName] = useState('');
  const [password1, setPassword1] = useState('');
  const [password2, setPassword2] = useState('');
  const [email, setUserEmail] = useState('');

  const [authToken, setAuthToken] = useState(null);

  const onChangeName = (e) => {
    setUserName(e.target.value);
  };
  const onChangePw1 = (e) => {
    setPassword1(e.target.value);
  };
  const onChangePw2 = (e) => {
    setPassword2(e.target.value);
  };
  const onChangeEmail = (e) => {
    setUserEmail(e.target.value);
  };

  const onSubmit = (e) => {
    e.preventDefault();

    const user = {
      username: name,
      password1: password1,
      password2: password2,
      email: email,
    };
    
    axios.post('http://localhost:8000/common/signup', user)
      .then(res => {
        console.log(res.data);
        setAuthToken(res.data.token);
      })
      .catch(err=>console.log(err));
  };

  return (
    <S.Wrap>
      <S.Container>
        <S.SignUpContainer signinIn={signIn}>
          <S.Form onSubmit={onSubmit}>
            <S.Title>Create Account</S.Title>
            <S.Input
              name="email" 
              type="email"
              placeholder="Email"
              value = {email}
              onChange={onChangeEmail}
              required
            />
            <S.Input
              name="password1"
              type="password"
              placeholder="Password"
              required=""
            />
            <S.Input
              name="password2"
              placeholder="Password Confirm"
              type="password"
              value={password2}
              required
              onChange={e => setPassword2(e.target.value)}
            />
            <S.Input
              name="username"
              type="text"
              placeholder="Name"
              value={name}
              onChange={onChangeName}
              required
            />
            <S.SignUpButton type="submit">Sign Up</S.SignUpButton>
          </S.Form>
        </S.SignUpContainer>

        <S.SignInContainer signinIn={signIn}>
          <S.Form>
            <S.Title>Sign in</S.Title>
            <S.Input 
              name="name"
              placeholder="Name"
              type="text"
              value={name}
              required
              onChange={e=>setUserName(e.target.value)}
            />
            <S.Input
              name="password1"
              placeholder="Password"
              type="password"
              value={password1}
              required
              onChange={e => setPassword1(e.target.value)}
            />
            {/* <S.Anchor href="#">Forgot your password?</S.Anchor> */}
            <S.Anchor href="#">Forgot your password?</S.Anchor>
            <S.SignInButton type="submit">Sign In</S.SignInButton>
          </S.Form>
        </S.SignInContainer>

        <S.OverlayContainer signinIn={signIn}>
          <S.Overlay signinIn={signIn}>
            <S.LeftOverlayPanel signinIn={signIn}>
              <S.Title>Welcome Back!</S.Title>
              <S.Paragraph>
                로그인하고 퀀티지가 제공하는<br></br>다양한 서비스를 경험하세요!
              </S.Paragraph>
              <S.GhostButton onClick={() => toggle(true)}>
                Sign In
              </S.GhostButton>
            </S.LeftOverlayPanel>

            <S.RightOverlayPanel signinIn={signIn}>
              <S.Title>Hello, QuantEZ</S.Title>
              <S.Paragraph>세상에서 가장 쉬운 투자, QuantEZ</S.Paragraph>
              <S.GhostButton onClick={() => toggle(false)}>
                Sign Up
              </S.GhostButton>
            </S.RightOverlayPanel>
          </S.Overlay>
        </S.OverlayContainer>
      </S.Container>
    </S.Wrap>
  );
};  