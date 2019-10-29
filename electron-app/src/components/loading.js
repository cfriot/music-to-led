
class Loading extends React.Component {

  constructor(props) {
    super(props);

    const sentences = [
      "Checking configuration file...",
      "Instanciating processes...",
      "Launching app...",
    ];

    this.state = { current_step: 0, total_steps: sentences.length, sentences: sentences };
  }

  componentDidMount() {
      this.intervalId = setInterval(() => this.setState({current_step: this.state.current_step + 1}), 2500);
  }

  render() {

    let is_finished = this.state.total_steps == this.state.current_step;

    if(is_finished) {
      clearInterval(this.intervalId);
    }

    let classes = is_finished ? "loading--invisible" : "loading"

    return <div className={classes}>
          <div>
            <img className="loading__logo" src="./img/logo.svg"/>
            <h1>AUDIO 2 LED</h1>
            <p>{this.state.sentences[this.state.current_step]}</p>
          </div>
        </div>;
  }
}
