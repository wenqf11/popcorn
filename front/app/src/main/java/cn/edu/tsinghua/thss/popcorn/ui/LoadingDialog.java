package cn.edu.tsinghua.thss.popcorn.ui;

import android.app.Dialog;
import android.content.Context;
import android.os.Handler;
import android.os.Message;
import android.util.AttributeSet;
import android.view.LayoutInflater;
import android.view.View;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import cn.edu.tsinghua.thss.popcorn.R;

/**
 * Created by 兜哥 on 2016/7/21.
 */
public class LoadingDialog extends View{
    private static final int DIALOG = 0;
    private static Handler handler=new Handler(){
        @Override
        public void handleMessage(Message msg) {
            switch (msg.what){
                case  DIALOG:
                    loadingDialog.dismiss();
            }
        }
    };
    private static Dialog loadingDialog;

    public LoadingDialog(Context context) {
        super(context);
        createLoadingDialog(context);
    }

    public LoadingDialog(Context context, AttributeSet attrs) {
        super(context, attrs);
        createLoadingDialog(context);
    }

    public LoadingDialog(Context context, AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
        createLoadingDialog(context);
    }

    /**
     * 得到自定义的progressDialog
     * @param context
     *
     * @return
     */
    public static Dialog createLoadingDialog(Context context) {

        LayoutInflater inflater = LayoutInflater.from(context);
        View v = inflater.inflate(R.layout.loding_dialog, null);// 得到加载view
        LinearLayout layout = (LinearLayout) v.findViewById(R.id.dialog_view);// 加载布局
        // main.xml中的ImageView
        ImageView spaceshipImage = (ImageView) v.findViewById(R.id.img);
        TextView tipTextView = (TextView) v.findViewById(R.id.tipTextView);// 提示文字
        // 加载动画
        Animation hyperspaceJumpAnimation = AnimationUtils.loadAnimation(
                context, R.anim.loading_animation);
        // 使用ImageView显示动画
        spaceshipImage.startAnimation(hyperspaceJumpAnimation);
//        tipTextView.setText(msg);// 设置加载信息

        // 创建自定义样式dialog
        loadingDialog = new Dialog(context, R.style.loading_dialog);

        loadingDialog.setCancelable(false);// 不可以用“返回键”取消
        loadingDialog.setContentView(layout, new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.FILL_PARENT,
                LinearLayout.LayoutParams.FILL_PARENT));// 设置布局
        handler.sendEmptyMessageDelayed(DIALOG,2000);
        return loadingDialog;

    }
}
