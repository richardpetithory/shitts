import {ApolloClient, from, HttpLink, InMemoryCache} from "@apollo/client";
import {loadDevMessages, loadErrorMessages} from "@apollo/client/dev";
import {removeTypenameFromVariables} from "@apollo/client/link/remove-typename";

if (import.meta.env.DEV) {
  loadDevMessages();
  loadErrorMessages();
}

const removeTypenameLink = removeTypenameFromVariables();

const httpLink = new HttpLink({
  uri: "http://localhost:8000/graphql/",
});

const client = new ApolloClient({
  link: from([removeTypenameLink, httpLink]),
  cache: new InMemoryCache(),
  defaultOptions: {
    watchQuery: {
      fetchPolicy: "no-cache",
      errorPolicy: "ignore",
    },
    query: {
      fetchPolicy: "no-cache",
      errorPolicy: "all",
    },
  },
});

export default client;
