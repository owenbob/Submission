/**
* This React class is intended to query an endpoint that will return an alphanumeric string, after clicking a button.
* This component is passed a prop "apiQueryDelay", which delays the endpoint request by N milliseconds. There is a 
* second button to disable this functionality and have the endpoint request run immediately after button click.
* This data is then to be displayed inside a simple container.
* The "queryAPI" XHR handler will return the endpoint response in the form of a Promise (such as axios, fetch).
* The response object will look like the following: {data: "A0B3HCJ"}
* The containing element ref isn't used, but should remain within the class.
* Please identify, correct and comment on any errors or bad practices you see in the React component class below.
* Additionally, please feel free to change the code style as you see fit.
* Please note - React version for this exercise is 15.5.4
*/

// Component should be destructured from 'react'
import React, { Component } from 'react';

import queryAPI from 'queryAPI';

/* import Button component from either third-party library or custom package 
  for example
*/
import Button from './Button'


class ShowResultsFromAPI extends Component {
  constructor(props) {
    super(props);
    this.container = null; 
    this.state = {
      data: '',
      // add error to state
      error: false,
      //
      apiQueryDelay: props.apiQueryDelay
    }
  }

  // Ideally modifying props should be done from outside the component
  // Arrow functions are also best practise
  onDisableDelay = () => {
    this.setState({apiQueryDelay: 0})
  }


  //Utilise arrow functions
  click = () => {
    console.log('Clicked!', {delay: this.state.apiQueryDelay});
    if (typeof this.state.apiQueryDelay === "number" && this.state.apiQueryDelay >= 0) {

      //Utilize arrow function
      setTimeout(() => {
        this.fetchData();
      }, this.state.apiQueryDelay);
    }
  }

  fetchData() {
    queryAPI()
      .then((response) => {
        if (response.data) {
          this.setState({
            data: response.data,
            error: false
          });
        }
      })

      // Good practise to catch errors incase anythin goes wrong
      .catch(() => {
        this.setState({data: '', error: true})
      });
  }

  render() {
    
    let msg = '';
    if (this.state.error) {
      msg = 'Sorry - there was an error with your request.';

    } else {
      msg = this.state.data;
    }

    return (
      // Render should return one root element
      <div>
        <div className="content-container" ref={node => this.container = node}>
          { 
          // Best not to have logic within the return
            msg && <p>{msg}</p>
          }
        </div>
        <Button onClick={this.onDisableDelay}>Disable request delay</Button>
        <Button onClick={this.click}>Request data from endpoint</Button>
      </div>
    );
  }
}

//displayName should be a string
ShowResultsFromAPI.displayName = "ShowResultsFromAPI";

ShowResultsFromAPI.defaultProps = {
  apiQueryDelay: 0
};

// React.propTypes should be Upper case
ShowResultsFromAPI.propTypes = {
  
  apiQueryDelay: React.PropTypes.number
};
// export as default export
export default ShowResultsFromAPI;
