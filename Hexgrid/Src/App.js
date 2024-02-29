import React, { Component } from 'react';
import TilesLayout from './TilesLayout';
import TilesLayoutLeft from './TilesLayoutLeft';


import { HexGrid, Layout, Hexagon, Text, Pattern, Path, Hex,HexUtils } from 'react-hexgrid';
import configs from './configurations';

import './App.css';

class App extends Component {

    // onDrop you can read information of the hexagon that initiated the drag
    onDrop(event, source, targetProps) {
      const { hexagons } = this.state;
      const hexas = hexagons.map(hex => {
        // When hexagon is dropped on this hexagon, copy it's image and text
        if (HexUtils.equals(source.state.hex, hex)) {
          hex.image = targetProps.data.image;
          hex.text = targetProps.data.text;
        }
        return hex;
      });
      this.setState({ hexagons: hexas });
    }
  
    onDragStart(event, source) {
      // If this tile is empty, let's disallow drag
      if (!source.props.data.text) {
        event.preventDefault();
      }
    }
  
    // Decide here if you want to allow drop to this node
    onDragOver(event, source) {
      // Find blocked hexagons by their 'blocked' attribute
      const blockedHexas = this.state.hexagons.filter(h => h.blocked);
      // Find if this hexagon is listed in blocked ones
      const blocked = blockedHexas.find(blockedHex => {
        return HexUtils.equals(source.state.hex, blockedHex);
      });
  
      const { text } = source.props.data;
      // Allow drop, if not blocked and there's no content already
      if (!blocked && !text) {
        // Call preventDefault if you want to allow drop
        event.preventDefault();
      }
    }
  
    // onDragEnd you can do some logic, e.g. to clean up hexagon if drop was success
    onDragEnd(event, source, success) {
      if (!success) {
        return;
      }
      // TODO Drop the whole hex from array, currently somethings wrong with the patterns
  
      const { hexagons } = this.state;
      // When hexagon is successfully dropped, empty it's text and image
      const hexas = hexagons.map(hex => {
        if (HexUtils.equals(source.state.hex, hex)) {
          hex.text = null;
          hex.image = null;
        }
        return hex;
      });
      this.setState({ hexagons: hexas });
    }

    onClick(event,source){
      alert("Great Shot!");
      return(<Path start={new Hex(0, 0, 0)} end={new Hex(-2, 0, 1)} />);
      // send message (Heaxagon cords clicked, item on tile)
      ///send message either get neighbours(hex: any) or neighbour(hex: any, direction: any)-
      
    }

    // handleClick() {
    //   alert('You clicked me!');
    // }
  render() {
    return (
      <div>
        <HexGrid width={1600} height={1000} viewBox="-50 -50 100 100">
          {/* Grid with manually inserted hexagons */}
          <Layout size={{ x: 6, y: 6 }} flat={true} spacing={1.03} origin={{ x: -20, y: -30 }}>
            <Hexagon q={0} r={0} s={0} ><Text> 0, 0, 0</Text> </Hexagon>
            {/* Using pattern (defined below) to fill the hexagon */}
            <Hexagon q={0} r={-1} s={1}  />
            <Hexagon q={0} r={1} s={-1}> <Text>0, 1, -1</Text> </Hexagon>
            <Hexagon q={1} r={-1} s={0}>
              <Text>1, -1, 0</Text>
            </Hexagon>
            <Hexagon 
            q={1} r={1} s={-2}
            onClick={(e, h) => this.onClick(e, h)}
            >
              
              <Text>Click me </Text>
            </Hexagon>
            <Hexagon q={1} r={0} s={-1}>
              <Text>1, 0, -1</Text>
            </Hexagon>
            <Hexagon q={2} r={0} s={-2}>
              <Text>2, 0, -2</Text>
            </Hexagon>
            {/* <Hexagon q={2} r={1} s={0}>
              <Text>2, 1, 0</Text>
            </Hexagon> */}
            <Hexagon q={2} r={-1} s={0}>
              <Text>2, -1, 0</Text>
            </Hexagon>
            <Hexagon q={2} r={-2} s={0}>
              <Text>2, -1, 0</Text>
            </Hexagon>
            <Hexagon q={0} r={2} s={-2}>
              <Text>0, 2, -2</Text>
            </Hexagon>
            <Hexagon q={3} r={-2} s={-1}>
              <Text>-3, -2, -1</Text>
            </Hexagon>
            <Hexagon q={3} r={-1} s={-2}>
              <Text>-3, -1, -2</Text>
            </Hexagon>
            {/* <Hexagon q={3} r={0} s={-3}>
              <Text>-3, -1, -2</Text>
            </Hexagon> */}
            {/* Pattern and text */}
            <Hexagon q={-1} r={1} s={0} >
              <Text>-1, 1, 0</Text>
            </Hexagon>
            <Hexagon q={-1} r={0} s={1} > <Text>-1, 0, 1</Text> </Hexagon>
            <Hexagon q={-2} r={0} s={1} fill="pat-1"> <Text>-2, 0, 1</Text></Hexagon>
            <Hexagon q={-1} r={2} s={-1} > <Text>-1, 2, -1</Text></Hexagon>
            <Hexagon q={-1} r={3} s={-1} > <Text>-1, 3, -1</Text></Hexagon>
            <Hexagon q={3} r={0} s={-3} > <Text>3, 0, -3</Text></Hexagon>
            <Hexagon q={3} r={1} s={-4} fill="pat-2"> <Text>3, 1, -4</Text></Hexagon>
            <Hexagon q={-2} r={1} s={1} > <Text>-2, 1, 1</Text></Hexagon>
            <Hexagon q={-2} r={2} s={0} > <Text>-2, 2, 0</Text></Hexagon>
            <Hexagon q={-2} r={3} s={-1} > <Text>-2, 3, -1</Text></Hexagon>
            <Hexagon q={-2} r={4} s={-2} > <Text>-2, 2, 0</Text></Hexagon>
            <Hexagon q={1} r={2} s={-2} > <Text>1, 2, -2</Text></Hexagon>
            <Hexagon q={2} r={1} s={-3} > <Text>2, 1, -3</Text></Hexagon>
            <Hexagon q={2} r={2} s={-4} > <Text>2, 2, -4</Text></Hexagon>









            {/* How to implment a path if wanted, could be useful if we want to show possible moves*/}
            {/* <Path start={new Hex(0, 0, 0)} end={new Hex(-2, 0, 1)} /> */}
          </Layout>
          <Pattern id="pat-1" link="https://th.bing.com/th/id/R.fc39510c20bb05962e9a6e848795eeba?rik=AaN5Owwu9hJLcQ&pid=ImgRaw&r=0" />
          <Pattern id="pat-2" link="https://tse1.mm.bing.net/th/id/OIP.pd31SnqlU3aAUQejZVbWUQHaFj?rs=1&pid=ImgDetMain" />
          <TilesLayout />
          <TilesLayoutLeft/>
        </HexGrid>
      </div>
    );
  }
}

export default App;