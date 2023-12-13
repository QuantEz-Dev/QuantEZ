import "../styles/Backtesting.scss";

export const BacktestingPort = () => {
  return (
    <div className="btWrapper">
      <div className="btContainer">
        <div className="btTitle">백테스팅 포트</div>
        <div className="loadBacktest" style={{marginTop: '2rem'}}>
          <iframe seamless src="http://localhost:8000/backtesting/" title="backtesting"/>
        </div>
      </div>
    </div>
  )
}