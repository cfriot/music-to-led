class StripVisualizer extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {

    let pixelsElems = [];
    let shape_offsets = [];
    let real_shape_offsets = [];

    if(this.props.active_shape) {
      this.props.active_shape.map((strip, index) => {
      	if(index - 1 >= 0) {
      		shape_offsets.push(strip + shape_offsets[index - 1]);
          }
      	else {
      		shape_offsets.push(strip);
          }
      });
    }

    if(this.props.real_shape) {
      this.props.real_shape.map((strip, index) => {
      	if(index - 1 >= 0) {
      		real_shape_offsets.push(strip + real_shape_offsets[index - 1]);
          }
      	else {
      		real_shape_offsets.push(strip);
          }
      });
    }

    if(this.props.pixels) {
      pixelsElems = this.props.pixels[0].map((pixel, index) => {

        let classes = "strip__led";
        shape_offsets.map((offset) => {
          if(index == offset) {
            classes = "strip__led strip__led--space2"
          }
        });
        real_shape_offsets.map((offset) => {
          if(index == offset) {
            classes = "strip__led strip__led--breakline2"
          }
        });

        return <div ref={pixel+index} className={classes} style={{backgroundColor: "rgb(" + this.props.pixels[0][index] + "," + this.props.pixels[1][index] + ", " + this.props.pixels[2][index] + ")"}}></div>
      });
    }

    return <div className='strip'>
          {pixelsElems}
        </div>;
  }
}
