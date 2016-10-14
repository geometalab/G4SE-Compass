import { Injectable } from '@angular/core';
import { Headers, Http, Response } from '@angular/http';

import 'rxjs/add/operator/toPromise';
import {Observable} from "rxjs/Observable";

import {SearchParameters} from "./search-parameters";
import {SearchResult} from "./search-result";

@Injectable()
export class SearchService {
  private metadataUrl = 'api/search/';  // URL to web API

  constructor(private http: Http) { }

  getSearchResultList(params: SearchParameters) {
    var headers = new Headers();
    headers.append('Content-Type', 'application/json; charset=utf-8');

    if (params == undefined) {
      params = new SearchParameters();
    }
    var urlParams = params.toUrlQuery();
    return this.http.get(this.metadataUrl + urlParams, {headers});
  }
}
