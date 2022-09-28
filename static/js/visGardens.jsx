
function SearchBox(props) {
    return (
        <form>
            <label htmlFor="search-terms">search by product, company, or keywords</label>
            <input type="text" name="search" id="search-terms" />
            <button onClick={(event) => {
                event.preventDefault();
                let searchBoxContents = document.getElementById('search-terms').value
                props.clickHandler(searchBoxContents)
            }}>Search</button>
        </form>
    );
}


function TableRow(props) {
    return (
        <tr>
            <td>{props.trade_name}</td>
            <td>{props.country}</td>
        </tr>
    );
}


// components take props
function CompanyTable(props) {
    const rows = [];

    /* Make some TableRows to put in our table*/
    if (props.data !== undefined && props.data.length) {
        for (let company of props.data) {
            rows.push(<TableRow key={company.id} {...company} />)
        }
        /* Return a html table with  our rows in the middle */
        return (
            <table>
                <thead>
                    <tr>
                        <td>trade_name</td>
                        <td>country</td>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        );
    } else {
        // props.data is empty - no data provided to the component
        return(<div></div>)
    }

}


/* This is a component to contain all the Components we want on our page */
function App(props) {
    const [searchResults, setSearchResults] = React.useState({ companies: [] })

    /**
     * Function that makes a fetch call to our /search.json route
     * gets a list of companies back and then sets the searchResults
     * state to the list of companies
     */
    const doSearch = (searchKeywords) => {
        fetch(`/search.json?search=${searchKeywords}`)
            .then((response) => response.json()) // converts the json text our flask route returned into an object
            .then((data) => {
                if (data !== undefined && data.length) {
                    setSearchResults({ companies: data })
                } else {
                    console.log(`No data returned for search [${searchKeywords}]`)
                }
            });
    }

    return (
        <div id='app'>
            <SearchBox clickHandler={doSearch} />
            <CompanyTable data={searchResults.companies} />
        </div>
    );
}



ReactDOM.render(<App />, document.getElementById('container'));