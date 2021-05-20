import React, {Component} from 'react';


import 'core-js/stable';
import 'regenerator-runtime/runtime';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import 'primeflex/primeflex.css';
import 'prismjs/themes/prism-coy.css';
import './assets/style/app/App.scss';

import {AppMenu} from './components/app/AppMenu';
import AppRouter from './components/app/AppRouter'
import AppNews from './components/app/AppNews';
import AppTopbar from './components/app/AppTopbar';
import AppFooter from './components/app/AppFooter';

// import AppContentContext from './AppContentContext';
import AppContentContext from './components/app/AppContentContext';
import PrimeReact from 'primereact/api';
import {classNames} from "primereact/components/utils/ClassNames";
import {Toast} from "primereact/toast";
import ReduxBlockUi from "react-block-ui/redux";
import 'react-block-ui/style.css';
import {ACTION} from "./redux/action";
import {connect} from "react-redux";
import {getContactInitData} from "./redux/action/initial";
import './App.css';

export class App extends Component {

    constructor(props) {
        super(props);

        this.news_key = 'primenews-react';
        this.theme_key = 'primetheme-react';

        this.state = {
            theme: 'bootstrap4-light-blue',
            inputStyle: 'outlined',
            ripple: false,
            darkTheme: false,
            themeCategory: null,
            sidebarActive: false,
            newsActive: false, //this.isNewsStorageExpired(),
            configuratorActive: false,
            changelogActive: false,
            searchVal: null,
        };

        this.onThemeChange = this.onThemeChange.bind(this);
        this.onMenuButtonClick = this.onMenuButtonClick.bind(this);
        this.onMenuItemClick = this.onMenuItemClick.bind(this);
        this.onHideNews = this.onHideNews.bind(this);
        this.onMaskClick = this.onMaskClick.bind(this);
        this.onInputStyleChange = this.onInputStyleChange.bind(this);
        this.onRippleChange = this.onRippleChange.bind(this);

        this.showChangelogDialog = this.showChangelogDialog.bind(this);
        this.hideChangelogDialog = this.hideChangelogDialog.bind(this);

        PrimeReact.ripple = false;
    }

    initTheme() {
        const queryString = window.location.search;
        const theme = queryString ? new URLSearchParams(queryString.substring(1)).get('theme') : localStorage.getItem(this.theme_key);

        if (theme) {
            const dark = this.isDarkTheme(theme);
            this.onThemeChange({
                theme,
                dark
            });
        }
    }

    onThemeChange(event) {
        let {theme, dark: darkTheme} = event;
        let themeElement = document.getElementById('theme-link');
        let themeCategory = /^(md-|mdc-)/i.test(theme) ? 'material' : (/^(bootstrap)/i.test(theme) ? 'bootstrap' : null);
        let state = {};

        if (theme.startsWith('md')) {
            PrimeReact.ripple = true;
            state = {ripple: true};
        }

        themeElement.setAttribute('href', themeElement.getAttribute('href').replace(this.state.theme, event.theme));

        state = {
            ...state, ...{
                theme,
                darkTheme,
                themeCategory
            }
        };

        this.setState(state, () => {
            localStorage.setItem(this.theme_key, this.state.theme);
        });
    }

    onMenuButtonClick() {
        this.menuClick = true;

        if (this.sidebarActive) {
            this.setState({sidebarActive: false});
            this.removeClass(document.body, 'blocked-scroll');
        } else {
            this.setState({sidebarActive: true});
            this.addClass(document.body, 'blocked-scroll');
        }
    }

    onMenuItemClick() {
        this.setState({sidebarActive: false});
        this.removeClass(document.body, 'blocked-scroll');
    }

    onMaskClick() {
        this.setState({sidebarActive: false});
        this.removeClass(document.body, 'blocked-scroll');
    }

    onHideNews(event) {
        this.setState({newsActive: false}, () => {
            const now = new Date();
            const item = {
                value: false,
                expiry: now.getTime() + 604800000,
            }
            localStorage.setItem(this.news_key, JSON.stringify(item));
        });
        event.stopPropagation();
    }

    isNewsStorageExpired() {
        const newsString = localStorage.getItem(this.news_key);
        if (!newsString) {
            return true;
        }
        const newsItem = JSON.parse(newsString);
        const now = new Date()

        if (now.getTime() > newsItem.expiry) {
            localStorage.removeItem(this.news_key);
            return true;
        }

        return false;
    }

    isDarkTheme(theme) {
        return /(dark|vela|arya|luna)/i.test(theme);
    }

    onInputStyleChange(inputStyle) {
        this.setState({inputStyle});
    }

    onRippleChange(value) {
        PrimeReact.ripple = value;

        this.setState({ripple: value});
    }

    showChangelogDialog(searchVal) {
        this.setState({
            changelogActive: true,
            searchVal
        });
    }

    hideChangelogDialog() {
        this.setState({changelogActive: false});
    }

    addClass(element, className) {
        if (element.classList)
            element.classList.add(className);
        else
            element.className += ' ' + className;
    }

    removeClass(element, className) {
        if (element.classList)
            element.classList.remove(className);
        else
            element.className = element.className.replace(new RegExp('(^|\\b)' + className.split(' ').join('|') + '(\\b|$)', 'gi'), ' ');
    }

    hasClass(element, className) {
        if (element.classList)
            return element.classList.contains(className);
        else
            return new RegExp('(^| )' + className + '( |$)', 'gi').test(element.className);
    }

    isOutdatedIE() {
        let ua = window.navigator.userAgent;
        if (ua.indexOf('MSIE ') > 0 || ua.indexOf('Trident/') > 0) {
            return true;
        }

        return false;
    }

    componentDidMount() {
        if (this.isOutdatedIE()) {
            this.showcaseToast.show({
                severity: 'warn',
                summary: 'Limited Functionality',
                detail: 'Although PrimeReact supports IE11, ThemeSwitcher in this application cannot be not fully supported by your browser. Please use a modern browser for the best experience of the showcase.',
                life: 6000
            });
        }

        this.initTheme();

        // get initial data
        this.props.getContactInitData();

    }

    render() {
        const wrapperClassName = classNames('layout-wrapper', {
            'layout-news-active': this.state.newsActive,
            'p-input-filled': this.state.inputStyle === 'filled',
            'p-ripple-disabled': this.state.ripple === false,
            [`theme-${this.state.themeCategory}`]: !!this.state.themeCategory
        });
        const maskClassName = classNames('layout-mask', {
            'layout-mask-active': this.state.sidebarActive
        });

        return (
            <div className={wrapperClassName}>
                <Toast ref={(el) => this.showcaseToast = el}/>

                <AppNews newsActive={this.state.newsActive} onHideNews={this.onHideNews}/>

                <AppTopbar onMenuButtonClick={this.onMenuButtonClick} onThemeChange={this.onThemeChange}
                           theme={this.state.theme} darkTheme={this.state.darkTheme}/>

                <AppMenu active={this.state.sidebarActive} onMenuItemClick={this.onMenuItemClick}/>

                <AppContentContext.Provider value={{
                    inputStyle: this.state.inputStyle,
                    darkTheme: this.state.darkTheme,
                    changelogText: "VIEW CHANGELOG",
                    onChangelogBtnClick: this.showChangelogDialog,
                    onInputStyleChange: this.onInputStyleChange
                }}>
                    <div className="layout-content">
                        <ReduxBlockUi block={ACTION.BLOCKER.BLOCK} unblock={ACTION.BLOCKER.UNBLOCK}
                                      onChange={(newValue, oldValue) => {
                                          return this.props.blocker.block;
                                      }}>
                            <AppRouter/>
                        </ReduxBlockUi>
                    </div>

                </AppContentContext.Provider>

                <div className={maskClassName} onClick={this.onMaskClick}></div>
            </div>
        );
    }
}


const mapStateToProps = (state) => ({
    blocker: state.blocker,
    initial: state.initial,
});

const mapDispatchToProps = () => {
    return {getContactInitData};
};

export default connect(mapStateToProps, mapDispatchToProps())(App);
