import React, {Component} from 'react';
import {Button} from "primereact/button";
import {Inplace} from "primereact/inplace";
import {classNames} from "primereact/components/utils/ClassNames";

class InputEditable extends Inplace {
    renderDisplay = (content) => {
        var className = classNames('p-inplace-display', {
            'p-disabled': this.props.disabled
        });
        return <div
            style={{display: 'block'}}
            className={className} onClick={this.open}
            onKeyDown={this.onDisplayKeyDown}
            tabIndex={this.props.tabIndex}
            aria-label={this.props.ariaLabel}
        >
            {content.props?.children ?? ''}
        </div>

    };

    renderCloseButton = () => {
        if (this.props.closable) {
            // return /*#__PURE__*/_react.default.createElement(_Button.Button, {
            //     type: "button",
            //     className: "p-inplace-content-close",
            //     icon: "pi pi-times",
            //     onClick: this.close
            // });

            return <Button type='button'
                           className='p-inplace-content-close p-button-outlined p-button-text p-button-success'
                           icon='pi pi-check'
                           onClick={this.close}/>
        }

        return null;
    }
}

export default InputEditable;