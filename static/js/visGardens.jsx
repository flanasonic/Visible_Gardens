const { MapboxOverlay } = deck;


// Create a nav bar
function NavBar(props) {

    return (<div className="navbar-items">
        <span>Products</span>
        <span>Companies</span>
        <span>Farms</span>
        <span>Data Maps</span>
        <span>News</span>
        <span onClick={props.contactMenuListener}>
            Contact
        </span>
    </div>)

}

// Components on this page ordered from smallest/finest to largest
function SearchBox(props) {
    return (
        <div className="searchbox-outline">
            <form>
                <input
                    id="search-terms"
                    name="search"
                    type="search"
                    autoComplete="off"
                    placeholder="Search..."
                />
                <button
                    onClick={(event) => {
                        event.preventDefault();
                        let searchBoxContents = document.getElementById('search-terms').value
                        props.clickHandler(searchBoxContents)
                    }}
                    className="search"
                ></button>
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
        <p>Address:<br></br>
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
    const coords = []
    for (let res of props.searchResults) {
        productDivs.push(
            <div key={res.product.id}
                onClick={() => updateMap(res.company.address.latitude, res.company.address.longitude)}
                className="search-results-item"
            >
                <div className="search-res-title">
                    <h2>{res.company.trade_name}</h2>
                </div>
                <div className="search-res-content">
                    <p>Product match: {res.product.name}</p>
                    <p>Description: {res.product.description}</p>
                    <AddressTemplate {...res.company.address} />
                </div>
            </div>
        )
        let addr = res.company.address
        coords.push([addr.longitude, addr.latitude])
    }
    if (coords.length > 0) {
        setMapIcons(coords)
        updateMap(coords[0][1], coords[0][0])
    }
    return (<div className="search-results-container">{productDivs}</div>
    )
}


// Our Shell component is the "vessel" for all of the other Components we want
// on our page
// React.useState returns a tuple of some stuff - our state object {companies: []}
// and setShellState -- changes the value of searchResults and lets the component 
// that takes searchResults as its props know that it's changed
function Shell(props) {
    const [shellState, setShellState] = React.useState({ searchResults: [] })
    const [contactFormState, setContactFormState] = React.useState({contactFormVisible: false})

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

    const toggleContactFormVis = () => {
        setContactFormState({contactFormVisible: !contactFormState.contactFormVisible})
    }

    return (
        <div id='app'>
            <div id="wrapper">
                <div id="navbar">
                    <NavBar contactMenuListener={toggleContactFormVis} />
                    <SearchBox clickHandler={doSearch} />
                </div>

                <div id="search-results">
                    <SearchResultsContainer searchResults={shellState.searchResults} />
                </div>
                <div id="map-container">

                </div>
                    {contactFormState.contactFormVisible ? <CompanyInfoForm doneHandler={toggleContactFormVis} /> : null}
            </div>
        </div>
    );
}


function CompanyInfoForm(props) {

    const companyFields = [
        ["Company Name", "company_name"],
        ["Type of Business", "business_type"],
        ["Website URL","website_url"],
        ["First Name", "first_name"],
        ["Last Name", "last_name"],
        ["email", "email"],
        ["phone number","phone"]
    ]

    let companyFieldInputs = []
    for (const [index, field] of companyFields.entries()) {
        companyFieldInputs.push(
            <div className="input-container" key={index} >
                <input className="comp-info-text-input" 
                name={field[1]} 
                onBlur={(event) => {
                    if (event.target.value) {
                      event.target.classList.add("is-valid");
                    } else {
                      event.target.classList.remove("is-valid");
                    }
                  }
                }
                ></input>
                <label htmlFor={field[1]} 
                    className="comp-info-label" 
                    onClick={ () => document.getElementsByName(field[1])[0].focus() }
                >{field[0]}</label>
            </div>
        )
    }
    return(
        <div className="contact-form" >
                <form>
                    <div className="comp-info-container" >
                        <span className="comp-info-form-title">Contact Us:</span>
                            {companyFieldInputs}
                            <button 
                                className="comp-info-submit-button"
                                onClick={(e) => {
                                        e.preventDefault();
                                        props.doneHandler();
                                    }
                                }
                                >Done</button>
                    </div>
                </form>
        </div>
    )
}




// the 'container' referenced here is the id of the div container in our
// jinja template
ReactDOM.render(<Shell />, document.getElementById('container'));





/***************************************************************
 * MAP Code
 */


mapboxgl.accessToken = 'pk.eyJ1IjoicHBhcnNvbnMiLCJhIjoiY2w4ejd5OTJwMDBqOTNubDE3ODh6emRvMiJ9.xQtkEA_3eGRcKssdvQ6zOw'

const map = new mapboxgl.Map({
    style: 'mapbox://styles/mapbox/streets-v11', // style URL
    center: [-73.98102176296132, 40.67115972631919], // starting position [lng, lat]
    zoom: 12, // starting zoom
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
    // map.invalidateSize();
    map.resize();


    map.loadImage('/static/images/tomato.png', (error, image) => {
        if (error) throw error;
        map.addImage('plant_icon', image);
    })
});

function updateMap(latitude, longitude) {
    map.flyTo({ center: [longitude, latitude], zoom: 9 })
}

function setMapIcons(coords) {
    if (!map) {
        console.log("map not loaded yet");
        return;
    }

    let farmMapSource = map.getSource('farms')

    if (farmMapSource) {
        map.removeLayer('farms').removeSource('farms')
    }

    let features = []

    for (let coord of coords) {
        features.push({
            'type': 'Feature',
            'properties': {},
            'geometry': {
                'type': 'Point',
                'coordinates': [coord[0], coord[1]]
            }
        })
    }

    map.addSource('farms', {
        'type': 'geojson',
        'data': {
            'type': 'FeatureCollection',
            'features': features
        }
    })

    map.addLayer({
        'id': 'farms',
        'type': 'symbol',
        'source': 'farms', // reference the data source
        'layout': {
            'icon-image': 'plant_icon', // reference the image
            'icon-size': 0.05
        }
    })
}
