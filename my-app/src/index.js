import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

class FSAItem extends React.Component {
  let description = []
  for(var i = 0; i < 3; i++){
    let squares = [];
    for(var j = 0; j < 3; j++){
      squares.push(this.renderSquare(i, j));
    }
    rows.push(<div className="board-row">{squares}</div>);
  }
  {% for description in p.description %}
  <li>{description}</li>
  {% endfor %}
  render(){
    <div class="dealbox">
      <div class="prodimage"> 
          <a href="{p.link}" target="_blank">
              <img src="{p.imagelink}" alt="{p.name}">
          </a>
      </div>
      {/* <div class="dealcontent">
          <strong>
              <a href="{p.link}" target="_blank">
                {p.name} -- ${p.price}
              </a>
          </strong>
          <div class="posttext">
              {p.category}
              <ul>
                {description}
              </ul>
          </div>
      </div>
      <div class="break"></div>
    </div> */}
  }
}

class FSAList extends React.Component {
  render 
}

function Square(props) {

  if (props.winner){
    return (
      <button className='square' style = "backgroundColor: '#00bcd4'" onClick={props.onClick}>
      {/* <button className='square'> */}
        {props.value}
      </button>
    );
  } else {
    return (
      <button className='square' onClick={props.onClick}>
      {/* <button className='square'> */}
        {props.value}
      </button>
    );
  }
}
class Board extends React.Component {
  renderSquare(i, j) {
    return (
      <Square 
        value = {this.props.squares[i][j]}
        onClick = {()=> this.props.onClick(i, j)} 
      />
    );
  }
  createSquares() {
    let rows = [];
    for(var i = 0; i < 3; i++){
      let squares = [];
      for(var j = 0; j < 3; j++){
        squares.push(this.renderSquare(i, j));
      }
      rows.push(<div className="board-row">{squares}</div>);
    }
    return rows;
  }

  render() {
    return (
      <div>
        {this.createSquares()}
      </div>
    );
  };
}

class Game extends React.Component {
  constructor(){
    super();
    this.state={
      history: [{
        squares: this.createArray(),
      }], 
      
      stepNumber: 0,
      xIsNext: true,
      ascending: true,
    };
  }
  toggleSort(){
    const ascending = this.state.ascending;
    this.setState({
      ascending:!ascending,
    });
  }
  createArray(){
    var arr = new Array(3);
    for (var i=0; i < 3; i++){
      arr[i] = new Array(3).fill(null)
    };
    return arr;
  }
  handleClick(i, j){
    const history = this.state.history.slice(0, this.state.stepNumber +1);
    const current = history[history.length-1];
    const squares = current.squares.map(function(arr) {
      return arr.slice();
    });
    if (calculateWinner(squares) || squares[i][j]){
      return;
    }
    console.log(squares)
    squares[i][j] = this.state.xIsNext ? 'X':'O';
    this.setState({
      history: history.concat([{
        squares: squares,
      }]),
      stepNumber: history.length,
      xIsNext: !this.state.xIsNext,
      });
    console.log(history)
  }

  jumpTo(step){
    this.setState({
      stepNumber: step,
      xIsNext: (step % 2)=== 0 
    });
    console.log(step)
  }

  render() {
    
    const history = this.state.history;
    const current = history[this.state.stepNumber];
    const winner = calculateWinner(current.squares);
    const ascending = this.state.ascending
    const moves = history.map((step, move)=>{
      const desc = move ?
        'Move #' + move:
        'Game start';
        return (
          <li key = {move}  >
            <a href = 'Move #' onClick={()=> this.jumpTo(move)}>{desc}</a>
          </li>
        );
    });

    let status;
    if (winner) {
      status = 'Winner: ' + winner;
    } else {
      status = 'Next player: ' + (this.state.xIsNext ? 'X' : 'O');
    }
    return (
      <div className="game">
        <div className="game-board">
          <Board 
            squares={current.squares}
            onClick={(i, j)=>this.handleClick(i, j)}
            />
        </div>
        <div className="game-info">
          <div>{status}</div>
            <button onClick={()=> this.toggleSort()}>
              Order
            </button>
            {(()=> this.state.ascending===true? <ol>{moves}</ol>:<ol>{moves.reverse()}</ol>)()}
        </div>
      </div>
    );
  }
}



// ========================================

ReactDOM.render(
  <Game />, 
  document.getElementById('root')
);

function calculateWinner(squares) {
  for (let i=0; i<squares.length; i++){
    if (squares[i][0]&& squares[i][0]===squares[i][1] &&
      squares[i][0] ===squares[i][2]){
        return squares[i][0];
      };
  };
  for (let i=0; i<squares.length; i++){
    if (squares[0][i]&& squares[0][i]===squares[1][0] &&
      squares[0][i] ===squares[2][i]){
        return squares[0][i];
      };
  };
  if (squares[0][0]&& squares[0][0]===squares[1][1] &&
    squares[0][0] ===squares[2][2]){
      return squares[0][0];
    };
  if (squares[0][2]&& squares[0][2]===squares[1][1] &&
    squares[0][2] ===squares[2][0]){
      return squares[0][2];
    };
  return null;
}
