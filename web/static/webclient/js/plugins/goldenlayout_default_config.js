var goldenlayout_config = {
    content: [{
        type: 'column',
        content: [{
            type: 'row',
            content: [{
                type: 'column',
                content: [{
                    type: 'component',
                    componentName: 'evennia',
                    componentId: 'evennia',
                    title: 'comms',
                    isClosable: false,
                    componentState: {
                        types: 'say',
                        updateMethod: 'append',
                    },
                }, {
                    type: 'component',
                    componentName: 'evennia',
                    componentId: 'evennia',
                    title: 'display',
                    height: 60,
                    isClosable: false,
                    componentState: {
                        types: 'look',
                        updateMethod: 'replace',
                    },
                }, {
                    type: 'component',
                    componentName: 'evennia',
                    componentId: 'evennia',
                    title: 'untagged',                    
                    isClosable: false,
                    componentState: {
                        types: 'untagged',
                        updateMethod: 'newlines',
                    },
                }],
            }, {
                type: 'column',
                content: [{
                    type: 'component',
                    componentName: 'Main',
                    isClosable: false,
                    tooltip: 'Main - drag to desired position.',
                    componentState: {
                        cssClass: 'content',
                        types: 'all',
                        updateMethod: 'newlines',
                    },
                }, {
                    type: 'component',
                    componentName: 'input',
                    id: 'inputComponent',
                    height: 10,
                    tooltip: 'Input - The last input in the layout is always the default.',
                }]
            }],
        }]
    }]
};