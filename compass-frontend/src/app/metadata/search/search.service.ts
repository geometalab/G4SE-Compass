import { Injectable } from '@angular/core';
import { Headers, Http, Response } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import {SearchParameters} from "./search-parameters";
import {SearchResult} from "./search-result";

@Injectable()
export class SearchService {
  private metadataUrl = 'api/search/';  // URL to web API

  constructor(private http: Http) { }

  getSearchResultList(params: SearchParameters=undefined): Promise<SearchResult[]> {
    if (params == undefined) {
      params = new SearchParameters();
    }
    var urlParams = params.toUrlQuery();
    return this.http
      .get(this.metadataUrl + urlParams)
      .toPromise()
      .then(response => response.json() as any[])
      .catch(this.handleError);
  }

  private handleError(error: any): Promise<SearchResult> {
    console.error('An error occurred', error);
    return Promise.reject(error.message || error);
  }
}
