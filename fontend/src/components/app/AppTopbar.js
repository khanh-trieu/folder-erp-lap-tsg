import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { CSSTransition } from 'react-transition-group';
import {Tooltip} from "primereact/tooltip";
import {Badge} from "primereact/badge";

// import { Tooltip } from './components/tooltip/Tooltip';
// import { Badge } from './components/badge/Badge';
// import { VersionService } from './showcase/service/VersionService';

export class AppTopbar extends Component {

    static defaultProps = {
        theme: null,
        darkTheme: false,
        onMenuButtonClick: null,
        onThemeChange: null
    };

    constructor(props) {
        super(props);

        this.state = {
            activeMenuIndex: null,
            versions: []
        };
        // this.versionService = new VersionService();

        this.logoMap = {
            'bootstrap4-light-blue': 'bootstrap4-light-blue.svg',
            'bootstrap4-light-purple': 'bootstrap4-light-purple.svg',
            'bootstrap4-dark-blue': 'bootstrap4-dark-blue.svg',
            'bootstrap4-dark-purple': 'bootstrap4-dark-purple.svg',
            'md-light-indigo': 'md-light-indigo.svg',
            'md-light-deeppurple': 'md-light-deeppurple.svg',
            'md-dark-indigo': 'md-dark-indigo.svg',
            'md-dark-deeppurple': 'md-dark-deeppurple.svg',
            'mdc-light-indigo': 'md-light-indigo.svg',
            'mdc-light-deeppurple': 'md-light-deeppurple.svg',
            'mdc-dark-indigo': 'md-dark-indigo.svg',
            'mdc-dark-deeppurple': 'md-dark-deeppurple.svg',
            'saga-blue': 'saga-blue.png',
            'saga-green': 'saga-green.png',
            'saga-orange': 'saga-orange.png',
            'saga-purple': 'saga-purple.png',
            'vela-blue': 'vela-blue.png',
            'vela-green': 'vela-green.png',
            'vela-orange': 'vela-orange.png',
            'vela-purple': 'vela-purple.png',
            'arya-blue': 'arya-blue.png',
            'arya-green': 'arya-green.png',
            'arya-orange': 'arya-orange.png',
            'arya-purple': 'arya-purple.png',
            'nova': 'nova.png',
            'nova-alt': 'nova-alt.png',
            'nova-accent': 'nova-accent.png',
            'luna-blue': 'luna-blue.png',
            'luna-green': 'luna-green.png',
            'luna-pink': 'luna-pink.png',
            'luna-amber': 'luna-amber.png',
            'rhea': 'rhea.png',
            'fluent-light': 'fluent-light.png',
            'soho-light': 'soho-light.png',
            'soho-dark': 'soho-dark.png',
            'viva-light': 'viva-light.svg',
            'viva-dark': 'viva-dark.svg',
            'mira': 'mira.jpg',
            'nano': 'nano.jpg'
        };

        this.onMenuButtonClick = this.onMenuButtonClick.bind(this);
        this.onThemeChange = this.onThemeChange.bind(this);
        this.onMenuEnter = this.onMenuEnter.bind(this);
        this.resetMenuActive = this.resetMenuActive.bind(this);

        this.themesOverlayRef = React.createRef();
        this.templatesOverlayRef = React.createRef();
        this.resourcesOverlayRef = React.createRef();
        this.versionsOverlayRef = React.createRef();
    }

    onMenuButtonClick(event) {
        if (this.props.onMenuButtonClick) {
            this.props.onMenuButtonClick(event);
        }
    }

    onThemeChange(event, theme, dark) {
        if (this.props.onThemeChange) {
            this.props.onThemeChange({
                originalEvent: event,
                theme,
                dark
            })
        }

        this.resetMenuActive();
    }

    toggleMenu(event, index) {
        this.setState((prevState) => ({
            activeMenuIndex: (prevState.activeMenuIndex === index) ? null : index
        }));
        event.preventDefault();
    }

    onMenuEnter() {
        this.bindOutsideClickListener();
    }

    resetMenuActive() {
        this.setState({ activeMenuIndex: null });
    }

    bindOutsideClickListener() {
        if (!this.outsideClickListener) {
            this.outsideClickListener = (event) => {
                if ((this.state.activeMenuIndex != null && this.isOutsideTopbarMenuClicked(event))) {
                    this.setState({ activeMenuIndex: null }, () => {
                        this.unbindOutsideClickListener();
                    });

                }
            };
            document.addEventListener('click', this.outsideClickListener);
        }
    }

    unbindOutsideClickListener() {
        if (this.outsideClickListener) {
            document.removeEventListener('click', this.outsideClickListener);
            this.outsideClickListener = null;
        }
    }

    isOutsideTopbarMenuClicked(event) {
        return !(this.topbarMenu.isSameNode(event.target) || this.topbarMenu.contains(event.target));
    }

    componentWillUnmount() {
        this.unbindOutsideClickListener();
    }

    render() {
        return (
            <div className="layout-topbar">
                <Tooltip target=".app-theme" position="bottom" />

                <button type="button" className="p-link menu-button" onClick={this.onMenuButtonClick} aria-haspopup aria-label="Menu">
                    <i className="pi pi-bars"/>
                </button>
                <Link to="/"  aria-label="PrimeReact logo" >
                    {/*<img alt="logo" src={`showcase/images/primereact-logo${this.props.darkTheme ? '' : '-dark'}.png`} />*/}
                    <h1 style={{margin: 0, color: 'var(--blue-500)'}}>ERP System</h1>
                </Link>
            </div>
        );
    }
}

export default AppTopbar;
