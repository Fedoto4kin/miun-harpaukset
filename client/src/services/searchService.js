import axios from '../axios';

export const fetchSearchSuggestions = async (query, reverse = false) => {
  try {
    const url = reverse ? 'v0/lexicon/reverse-search-suggestions/' : 'v0/lexicon/search-suggestions/';
    const response = await axios.get(url, { params: { query } });
    return response.data;
  } catch (error) {
    console.error('Error fetching search suggestions:', error);
    throw error;
  }
};