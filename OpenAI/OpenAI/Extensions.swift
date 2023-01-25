//
//  Extensions.swift
//  OpenAI
//
//  Created by Colby L Williams on 1/24/23.
//

import SwiftUI
import SwiftyChat

internal extension TextCellStyle {
    static func getMessageCellStyle(isSender: Bool) -> TextCellStyle {
        let textColor = Color(isSender ? "MessageTextOutgoing" : "MessageTextIncoming")
        let backgroundColor = Color(isSender ? "MessageBackgroundOutgoing" : "MessageBackgroundIncoming")
        return TextCellStyle(
            textStyle: .init(
                textColor: textColor,
                font: .body,
                fontWeight: .regular
            ),
            textPadding: 12,
            attributedTextStyle: .init(
                textColor: UIColor(textColor),
                font: .monospacedSystemFont(ofSize: 17, weight: .semibold),
                fontWeight: .semibold
            ),
            cellBackgroundColor: backgroundColor,
            cellCornerRadius: 16,
            cellBorderColor: .clear,
            cellBorderWidth: 0,
            cellShadowRadius: 0,
            cellShadowColor: .clear,
            cellRoundedCorners: .allCorners
        )
    }
}

internal extension AvatarStyle {
    static let defaultStyle: AvatarStyle = AvatarStyle(
        imageStyle: .init(
            imageSize: .init(width: 32, height: 32),
            cornerRadius: 16,
            borderColor: .clear,
            borderWidth: .zero,
            shadowRadius: 1,
            shadowColor: .secondary
        ),
        avatarPosition: .alignToMessageTop(spacing: 6)
    )
}

internal extension ChatMessageCellStyle {
        
    static let OpenAIStyle = ChatMessageCellStyle(
        incomingTextStyle: TextCellStyle.getMessageCellStyle(isSender: false),
        outgoingTextStyle: TextCellStyle.getMessageCellStyle(isSender: true),
        incomingCellEdgeInsets: EdgeInsets(top: 2, leading: 4, bottom: 2, trailing: 50),
        outgoingCellEdgeInsets: EdgeInsets(top: 2, leading: 50, bottom: 2, trailing: 4),
        incomingAvatarStyle: AvatarStyle.defaultStyle,
        outgoingAvatarStyle: AvatarStyle.defaultStyle
    )
}
