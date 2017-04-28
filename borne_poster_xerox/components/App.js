import React from 'react';
import ReactDOM from 'react-dom';


class App extends React.Component {
	render () {
		return (
			<div>
				<form action="/print" method="post">
				  Code: <input type="text" name="code"/><br/>
				  <input type="submit" value="Submit"/>
				</form>
			</div>
		)
	}
}

export default App