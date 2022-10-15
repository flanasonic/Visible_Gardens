const { MapboxOverlay } = deck;


// Components on this page ordered from smallest/finest to largest
function SearchBox(props) {
    return (
        <div id="searchbox" className="row">
        <form>
            <label htmlFor="search-terms">search products</label>
            <input type="text" name="search" id="search-terms" />
            <button onClick={(event) => {
                event.preventDefault();
                let searchBoxContents = document.getElementById('search-terms').value
                props.clickHandler(searchBoxContents)
            }}>Search</button>
        </form>
        </div>
    );
}

function FacilityCard(props) {
    const facilityDivs = []
    for (let fac of res.facilities) {
        facilityDivs.push(
            <div key={fac.id} onClick={() => updateMap(fac.address.latitude, fac.address.longitude)}>
                <p>Facility: {fac.nickname} {fac.address.latitude} {fac.address.longitude}</p>
            </div>
        )
    }
}



function AddressTemplate(props) {
    return (<div key={props.id}>
        <p>Company address:<br></br> 
        {props.address_1} {props.address_2} {props.suite}<br></br> 
        {props.city}, {props.state}, {props.postal}, {props.country}</p>
    </div>)
}

/**
 * Expects a props object with a searchResults
 * prop that has a list of all our db.model
 * objects 
 * 
 * @param {*} searchResults 
 * @returns 
 */
function SearchResultsContainer(props) {
    const productDivs = []
    for (let res of props.searchResults) {
        productDivs.push(
            <div key={res.product.id}
                onClick={() => updateMap(res.company.address.latitude, res.company.address.longitude)}>
                <h2>{res.company.trade_name}</h2>
                <p>Product match: {res.product.name}</p>
                <p>Description: {res.product.description}</p>
                <AddressTemplate {...res.company.address}/> 
              
            </div>
        )
        console.log(props.searchResults)
    }
    return (<div>{productDivs}</div>
    )

}




// Our Shell component is the "vessel" for all of the other Components we want
// on our page
// React.useState returns a tuple of some stuff - our state object {companies: []}
// and setShellState -- changes the value of searchResults and lets the component 
// that takes searchResults as its props know that it's changed
function Shell(props) {
    const [shellState, setShellState] = React.useState({ searchResults: [] })

    /**
     * Function that makes a fetch call to our /search.json route
     * gets a list of companies back and then sets the searchResults
     * state to the list of companies
     */
    const doSearch = (searchKeywords) => {
        fetch(`/search.json?search=${searchKeywords}`)  // calls get_results() function from server.py
            .then((response) => response.json()) // converts the json text our flask route returned into an object
            .then((data) => {
                if (data !== undefined && data.length) {
                    setShellState({ searchResults: data })
                } else {
                    console.log(`No data returned for search [${searchKeywords}]`)
                }
            });
    }

    return (
        <div id='app'>
            <div id="wrapper">
                <div id="navbar">
                    <SearchBox clickHandler={doSearch} />
                </div>

                <div id="search-results">
                    <SearchResultsContainer searchResults={shellState.searchResults} />
                </div>
                <div id="map-container">

                </div>
            </div>
        </div>
    );
}

// the 'container' referenced here is the id of the div container in our
// jinja template
ReactDOM.render(<Shell />, document.getElementById('container'));

mapboxgl.accessToken = 'pk.eyJ1IjoicHBhcnNvbnMiLCJhIjoiY2w4ejd5OTJwMDBqOTNubDE3ODh6emRvMiJ9.xQtkEA_3eGRcKssdvQ6zOw'

const map = new mapboxgl.Map({

    style: 'mapbox://styles/mapbox/streets-v11', // style URL
    center: [-74.5, 40], // starting position [lng, lat]
    zoom: 9, // starting zoom
    projection: 'globe', // display the map as a 3D globe,
    container: 'map-container',
    followUserLocation: false,
    mapboxApiAccessToken: 'pk.eyJ1IjoicHBhcnNvbnMiLCJhIjoiY2w4ejd5OTJwMDBqOTNubDE3ODh6emRvMiJ9.xQtkEA_3eGRcKssdvQ6zOw',
    layers: [
    ]
});

map.on('load', () => { map.resize(); });
map.on('style.load', () => {
    map.setFog({}); // Set the default atmosphere style
    map.invalidateSize();
    map.resize();
});

function updateMap(latitude, longitude) {
    //alert(`Flying to coordinates ${latitude} ${longitude}`)
    map.flyTo({ center: [longitude, latitude], zoom: 9 })
}