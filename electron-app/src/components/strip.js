class Strip extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {

    {
      /*
      // active_audio_channel_index
      // active_color_scheme_index
      // active_shape_index
      // active_visualizer_effect
      // associated_midi_channels
      // bpm
      // color_schemes
      // formatted_color_schemes
      // is_mirror
      // is_reverse
      // max_brightness
      // midi_ports_for_changing_mode
      // name
      // number_of_color_schemes
      // number_of_shapes
      // real_shape
      // serial_port_name
      // "/dev/tty.usbserial-14220"
      // shapes

      active_shape = this.props.strip.shapes[this.props.strip.active_shape_index];
      active_color_scheme = this.props.strip.color_schemes[this.props.strip.active_color_scheme_index];

      */
    }


    let active_shape = this.props.strip.shapes[this.props.strip.active_shape_index].shape;
    let active_color_scheme = this.props.strip.color_schemes[this.props.strip.active_color_scheme_index];

    let is_reverse = this.props.strip.is_reverse.toString();
    let is_mirror = this.props.strip.is_mirror.toString();
    let bpm = this.props.strip.bpm;

    let colorSchemeElem = [];
    colorSchemeElem = active_color_scheme.map((color, index) => {
      return <div ref={color+index} className="strip__color" style={{backgroundColor: color}}></div>
    });

    let onlineClassNames = this.props.strip.is_online?" online":" offline"

    return <div className='card strip-block'>

        <div className={"online-notifier" + onlineClassNames} >
          <label className="online-notifier__label">online</label>
          <div className="online-notifier__circle"></div>
        </div>
        <h4 className="card__title">{this.props.strip.name} on <span className="strip__value">{ this.props.strip.active_visualizer_effect }</span></h4>
        <p>
          <span className="strip__label">Color</span> <span className="strip__value">{ colorSchemeElem }</span>
          <span className="strip__label">Bpm</span> <span className="strip__value">{ bpm }</span>
          <span className="strip__label">Audio channel</span> <span className="strip__value">{ this.props.config.audio_ports[this.props.strip.active_audio_channel_index].name }</span>
          <span className="strip__label" style={{opacity:this.props.strip.is_reverse?0.5:1}}>Reverse</span>
          <span className="strip__label" style={{opacity:this.props.strip.is_mirror?0.5:1}}>Mirror</span>
        </p>

        <StripVisualizer real_shape={this.props.strip.real_shape} active_shape={active_shape} pixels={this.props.pixels} />

        <MidiVisualizer midi_datas={this.props.strip.midi_logs}/>

      </div>;

  }
}
