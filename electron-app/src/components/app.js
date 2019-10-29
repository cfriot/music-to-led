const zerorpc = require("zerorpc")
let client = new zerorpc.Client()
client.connect("tcp://127.0.0.1:8000");

class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = { config: null, strips: null, audios: null };
  }
  componentDidMount() {
    this.intervalId = setInterval(() => this.loadData(), 50);
  }

  componentWillUnmount() {
    clearInterval(this.intervalId);
  }

  loadData() {

    client.invoke("getInfos", "ok", (error, res) => {

      if(error) {
        console.error(error)
      } else {

        res = JSON.parse( res );

        console.log(res);

        this.setState({
          config: res.config,
          audios: res.audios,
          strips: res.strips
        });

      }

    });

  }

  render() {

    let audiosElem = [];
    let stripsElem = [];

    if(this.state.audios && this.state.config && this.state.strips) {

      audiosElem = this.state.audios.map((audio, index) => {
        return <AudioVisualizer ref={audio + index} name={this.state.config.audio_ports[index].name} audio={this.state.audios[index]} />
      });
      stripsElem = this.state.strips.map((strip, index) => {
        return <Strip ref={strip + index} pixels={this.state.strips[index]} strip={this.state.config.strips[index]}/>
      });

    }

    return <div id="app">
      <Loading/>
      <div style={{display:"flex"}}>
        {/* <div style={{width:"50%"}}>
          <h4 className="title">Midi channels #4</h4>
          <MidiConsole/>
        </div> */}
        <div style={{width:"50%"}}>
          <h4 className="title"><span>{audiosElem.length}</span> Audio channel{audiosElem.length > 1 ? "s" : "" } </h4>
          {audiosElem}
        </div>
      </div>
      <h4 className="title"><span>{stripsElem.length}</span> Strip{stripsElem.length > 1 ? "s" : "" }</h4>
      {stripsElem}
    </div>
  }

}
