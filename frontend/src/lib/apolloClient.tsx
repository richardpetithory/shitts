import {ApolloClient, InMemoryCache} from "@apollo/client";
import {loadDevMessages, loadErrorMessages} from "@apollo/client/dev";

// if (import.meta.env.DEV) {
console.log("Loading");
loadDevMessages();
loadErrorMessages();
// }

const client = new ApolloClient({
  uri: "http://localhost:8000/graphql/",
  cache: new InMemoryCache(),
});

export default client;
